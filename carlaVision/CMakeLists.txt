cmake_minimum_required(VERSION 3.0.2)
project(carlaVision)


find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

find_package(OpenCV REQUIRED)

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate services in the 'srv' folder
# add_service_files(
#   FILES
#   Service1.srv
#   Service2.srv
# )

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
# generate_messages(
#   DEPENDENCIES
#   sensor_msgs#   std_msgs
# )


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES carlaVision
#  CATKIN_DEPENDS cv_bridge image_transport roscpp rospy sensor_msgs std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(lanedetect src/lanedetect.cpp)
target_link_libraries(lanedetect
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
)

add_executable(saveImage src/saveImage.cpp)
target_link_libraries(saveImage
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
)