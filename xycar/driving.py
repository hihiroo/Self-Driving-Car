#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2, math
import rospy, rospkg, time
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped

from cv_bridge import CvBridge
from xycar_msgs.msg import xycar_motor
from math import *
import signal
import sys
import os
import random

import time


def signal_handler(sig, frame):
    import time
    time.sleep(3)
    os.system('killall -9 python rosout')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Robotvisionsystem:
    def __init__(self):
        self.image = np.empty(shape=[0])
        self.realimage = np.empty(shape=[0]) 
        self.bridge = CvBridge() 
        self.motor = None 
        self.angle = 0
        self.speed = 0.5
        self.stop = 0

        self.CAM_FPS = 30
        self.WIDTH, self.HEIGHT = 640, 480

        rospy.init_node('driving')
        
        # self.motor = rospy.Publisher('/xycar_motor', xycar_motor, queue_size=1)
        # self.real_image = rospy.Subscriber('/usb_cam/image_raw/compressed',CompressedImage, self.realimg_callback)

        self.unitymotor = rospy.Publisher('/unitymotor', PoseStamped, queue_size=1)
        self.unity_img = rospy.Subscriber('/unitycamera', CompressedImage , self.img_callback)

        print("----- Xycar self driving -----")
        self.start()    

    def img_callback(self, data):
        # print data
        try:
            self.image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8") # mono8, mono16, bgr8, rgb8, bgra8, rgba8, passthrough
        except CvBridgeError as e:
            print("___Error___")
            print(e)
        
        # np_arr = np.formstring(data, np.unit8)
        # self.image = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    
    def realimg_callback(self, data):
        # print data
        try:
            self.realimage = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8") # mono8, mono16, bgr8, rgb8, bgra8, rgba8, passthrough
        except CvBridgeError as e:
            print("___Error___")
            print(e)
        
        # np_arr = np.formstring(data, np.unit8)
        # self.image = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    
    def trackbar(self):
        img = self.image
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        cv2.namedWindow("TrackBar Windows")
        cv2.setTrackbarPos("L-High","TrackBar Windows", 255)
        cv2.setTrackbarPos("L-Low" ,"TrackBar Windows", 0)
        print ":::::"
        while cv2.waitKey(1) != ord('q'):
            L_h = cv2.getTrackbarPos("L-High", "TrackBar Windows")
            L_l = cv2.getTrackbarPos("L-Low" , "TrackBar Windows")
            HLS = cv2.inRange(hls, (0, L_l, 0), (255, L_h, 255))
            hls_out = cv2.bitwise_and(hls, hls, mask = HLS)
            result = cv2.cvtColor(hls_out, cv2.COLOR_HSV2BGR)
            cv2.imshow("TrackBar Windows", result)
        
        cv2.destoryAllWindows()

    def drive(self, angle, speed):
        
        motor_msg = xycar_motor()
        motor_msg.angle = angle
        motor_msg.speed = speed

        self.motor.publish(motor_msg)

    def unitydrive(self, angle, speed):

        unitymotor_msg = PoseStamped()
        unitymotor_msg.pose.position.x = speed
        unitymotor_msg.pose.orientation.x = angle

        self.unitymotor.publish(unitymotor_msg) 

    def start(self):
        while not self.image.size == (self.WIDTH * self.HEIGHT * 3):
            continue
        print("==> Complete Load Image ")

        
        while not rospy.is_shutdown(): # Main Loop
            # HLS Ckeck
            # self.trackbar()
            
            # Task1 : White, Yellow line detection
            # Task2 : Traffic light -> Stop or Turn Left
            # Task3 : 90 degree line
            # Task4 : Finish line

            
            self.current_time = rospy.get_time()
            
            if self.stop == 0:
                img = self.image.copy()
                blur = cv2.GaussianBlur(img, (5, 5), 0)
                canny = cv2.Canny(blur, 100, 200)
                _, canny = cv2.threshold(canny, 100, 255, cv2.THRESH_BINARY)

                mask = np.zeros((self.HEIGHT, self.WIDTH), dtype=np.uint8)
                mask[400:self.HEIGHT, 100:self.WIDTH-100] = 255
                canny = cv2.bitwise_and(canny, mask)

                lines = cv2.HoughLinesP(canny, 1, math.pi/180, 20, 30, 20)
                Rdetect, Ldetect = 0, 0
                slope_thresh = 0.2
                selected_line = []

                if lines is not None:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        ini = [x1, y1]
                        fini = [x2, y2]

                        slope = (fini[1] - ini[1]) / (fini[0]-ini[0] + 0.00001)

                        if abs(slope) > slope_thresh:
                            selected_line.append([slope, line[0]])

                center = self.WIDTH / 2
                Lline, Rline = [], []

                for line in selected_line:
                    x1, y1, x2, y2 = line[1]
                    slope = line[0]
                    ini = [x1, y1]
                    fini = [x2, y2]
                    
                    if ini[0] > center:
                        Rline.append(line[1])
                        Rdetect = 1
                    elif ini[0] < center:
                        Lline.append(line[1])
                        Ldetect = 1
        
                lp, rp = [], []

                test = img.copy()

                if Rdetect:
                    for line in Rline:
                        right_points = [[line[0], line[1]], [line[2], line[3]]]
                        vx, vy, x, y = cv2.fitLine(np.array(right_points), cv2.DIST_L2, 0, 0.01, 0.01)
                        xx = (self.HEIGHT - y) // (vy/vx) + x
                        yy = (400 - y) // (vy/vx) + x
                        #cv2.line(test, (xx, self.HEIGHT), (yy, 400), (0,0,0), 4, 8)

                        if len(rp) == 0 or rp[0] > xx: 
                            rp = [xx, yy]
                
                if Ldetect:
                    for line in Lline:
                        left_points = [[line[0], line[1]], [line[2], line[3]]]
                        vx, vy, x, y = cv2.fitLine(np.array(left_points), cv2.DIST_L2, 0, 0.01, 0.01)
                        xx = (self.HEIGHT - y) // (vy/vx) + x
                        yy = (400 - y) // (vy/vx) + x
                        #cv2.line(test, (xx, self.HEIGHT), (yy, 400), (0,0,0), 4, 8)


                        if len(lp) == 0 or lp[0] < xx: 
                            lp = [xx, yy]
                
                lx, rx = 0, self.WIDTH
                if len(lp) != 0:
                    #v2.line(test, (lp[0], self.HEIGHT), (lp[1], 400), (255,0,0), 4, 8)
                    lx = (lp[1] + lp[0]) // 2
                if len(rp) != 0:
                    #cv2.line(test, (rp[0], self.HEIGHT), (rp[1], 400), (0,0,255), 4, 8)
                    rx = (rp[1] + rp[0]) // 2

                if not (lx == 0 and rx == self.WIDTH):
                    center = (lx + rx) // 2
                    cv2.line(test,(center, 400), (center, 400), (0,0,255),3)

                    self.angle = -(center - (self.WIDTH//2))
                    if self.angle > 100:
                        self.angle = 100
                        self.speed = 0.2
                    elif self.angle < -100:
                        self.angle = -100
                        self.speed = 0.2
                    elif abs(self.angle) < 20:
                        self.angle = 0
                        self.speed = 0.7
                    else:
                        self.speed = 0.5


               

            # ## Stop line ROI Area ##########################################
            # #640x480
            # stop_x_min = 240
            # stop_x_max = 400
            # stop_y_min = 370
            # stop_y_max = 410
            # stop_roi = L.copy()
            # stop_roi = stop_roi[stop_y_min:stop_y_max, stop_x_min:stop_x_max] # y,x
            # # try:
            # _, contours, _ = cv2.findContours(stop_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # # print("contours : ", contours)
            # for cont in contours:
            #     length = cv2.arcLength(cont, True)
            #     area = cv2.contourArea(cont)
            #     # print("Stop Flag : ", self.stop, "Area :", area, "Length : ", length)

            #     if not ((2000 > area > 1200) and (length > 300)):
            #         continue

            #     # print("Len : ", len(cv2.approxPolyDP(cont, length*0.02, True)))
            #     if len(cv2.approxPolyDP(cont, length*0.02, True)) < 2:
            #         continue
                
            #     (x, y, w, h) = cv2.boundingRect(cont)
            #     center = (x + int(w/2), y + int(h/2))

            #     if (70 <= center[0] <= (stop_x_max - stop_x_min)) and (self.stop == 0):
            #         cv2.rectangle(self.image, (x+stop_x_min, y+stop_y_min), (x + w + stop_x_min, y + h + stop_y_min), (0, 255, 0), 2)
            #         self.stop += 1
            #         self.past_time = self.current_time
            #         print "stopline"
                
            #     if self.stop == 1:
            #         print("Flag stop == 1")
            #         self.past_time = self.current_time
            #         while self.current_time - self.past_time <= 5:
            #             self.current_time = rospy.get_time()
            #             self.angle = 0
            #             self.speed = 0
            #             self.drive(self.angle, self.speed)                    
            #             print ("Stop ", str(self.current_time - self.past_time), "sec")

            #         self.past_time = self.current_time
                    
            #         self.past_time = self.current_time
            #         while self.current_time - self.past_time <= 2:
            #             self.current_time = rospy.get_time()
            #             self.angle = 0
            #             self.speed = 5
            #             self.drive(self.angle, self.speed)                    
            #             print ("After stop, Go ", str(self.current_time - self.past_time), "sec")
                    
            #         self.stop = 0
            #         self.speed = 1

            # except:
            #     print("Error yellowline")
            
            # Draw Stopline Area x,y
            #cv2.rectangle(self.image, (stop_x_min, stop_y_min), (stop_x_max, stop_y_max), (0, 0, 255), 2)
            ###############################################################
            

            # self.angle = -30
            # self.speed = 0
            
            # Publish xycar motor & unity motor
            self.unitydrive(self.angle, self.speed)
            
            # Check Image
            original_img = self.image.copy()
            cv2.putText(original_img, 'Time : ', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)
            cv2.putText(original_img, str(self.current_time), (80, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)
            cv2.putText(original_img, 'Speed : ', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)
            cv2.putText(original_img, str(self.speed), (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)
            cv2.putText(original_img, 'Angled : ', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)
            cv2.putText(original_img, str(self.angle), (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 125, 125), 1, cv2.LINE_AA)

            
            robotvision_horizontal = np.hstack((test, original_img))
            cv2.imshow("RobotVision", robotvision_horizontal)
            cv2.waitKey(1)
            
            
            
if __name__ == '__main__':
    RVS = Robotvisionsystem()

