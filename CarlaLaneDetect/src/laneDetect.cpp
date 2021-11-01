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
    image_transport::ImageTransport it;
    image_transport::Subscriber getImage;
    image_transport::Publisher pubLaneImage;
    bool isRun;

    Subscribe_And_Publish(bool isrun): isRun(isrun), it(n){
        getImage = it.subscribe("/carla/ego_vehicle/camera/rgb/front/image_color", 1, &Subscribe_And_Publish::callback, this);
        pubLaneImage = it.advertise("/laneImage",1);
    }

    void callback(const sensor_msgs::ImageConstPtr& img){
        // sensor_msgs/Image -> opencv Mat type images
        cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(img, sensor_msgs::image_encodings::MONO8); // img를 인코딩하여 opencv Image타입으로 변환
        Canny(cv_ptr->image, cv_ptr->image, 100, 200);
        pubLaneImage.publish(cv_ptr->toImageMsg()); // opencv Mat type -> sensor_msgs/Image type
    }
};

int main(int argc, char **argv){
    cout << "Start laneDetect node!\n";
    ros::init(argc, argv, "laneDetect");

    Subscribe_And_Publish laneDetect(1);
    ros::spin();
}
