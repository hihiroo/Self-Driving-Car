#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>
#include <image_transport/image_transport.h>
#include <ros/ros.h>
#include <vector>
#include <iostream>
#include <string>
using namespace std;
using namespace cv;

int i=0;

void callback(const sensor_msgs::ImageConstPtr& img){
    cv_bridge::CvImagePtr cv_ptr;
    cv_ptr = cv_bridge::toCvCopy(img, sensor_msgs::image_encodings::BGR8);
    
    string path = "/home/hihiroo/bagfiles/image1/carlaImage";
    path += to_string(i) + ".png";
    if(i++ % 10 == 0) imwrite(path, cv_ptr->image);
}

int main(int argc, char **argv){
    cout << "Start laneDetect node!\n";
    ros::init(argc, argv, "saveImage");

    ros::NodeHandle n;
    image_transport::ImageTransport it(n);

    image_transport::Subscriber sub = it.subscribe("/carla/ego_vehicle/camera/rgb/front/image_color", 10, callback);
    
    ros::spin();
}
