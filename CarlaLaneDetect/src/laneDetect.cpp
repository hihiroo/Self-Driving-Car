#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>
#include <image_transport/image_transport.h>
#include <ros/ros.h>
#include <vector>
#include <iostream>
using namespace std;
using namespace cv;

struct Subscribe_And_Publish{
    ros::NodeHandle n;
    ros::Subscriber getImage;
    ros::Publisher pubLaneImage;
    bool isRun;

    Subscribe_And_Publish(bool isrun): isRun(isrun){
        getImage = n.subscribe("/carla/ego_vehicle/camera/rgb/front/image_color", 10, &Subscribe_And_Publish::callback, this);
        pubLaneImage = n.advertise<sensor_msgs::Image>("laneImage",10);
    }

    void callback(const sensor_msgs::Image img){
        pubLaneImage.publish(img);
    }
};

int main(int argc, char **argv){
    cout << "Start laneDetect node!\n";
    ros::init(argc, argv, "laneDetect");

    Subscribe_And_Publish laneDetect(1);
    ros::spin();
}
