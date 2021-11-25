```shell
ros_ws/
    build
    devel
    logs
    src/
        carlaVision
        darknet_ros
        ros-bridge
```

1. ros_ws/ 에서 catkin_make로 빌드
2. darknet_ros/darknet_ros/config/ros.yaml의 camera_reading topic과 darknet_ros/darknet_ros/launch/darknet_ros.launch의 image arg defalut를 /laneImage로 변경  
3. roslaunch carlaVision carla_vision.launch로 신호등 검출 및 차선 검출 실행  


