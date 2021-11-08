cmake_minimum_required(VERSION 3.0.2)
project(withCarla)


find_package(catkin REQUIRED COMPONENTS # catkin 변수에 components 패키지들이 추가됨.
  roscpp # 즉 catkin_INCLUDE_DIRS에 catkin 뿐만 아니라 components로 추가된 패키지 경로까지 한번에 저장됨 => 관리가 쉬워짐
  rospy
  cv_bridge
  std_msgs
  sensor_msgs
  image_transport  
)
find_package(OpenCV REQUIRED) # 단, opencv 같이 런타임에 실행되는 패키지는 components로 쓸 수 없음 => OpenCV_INCLUDE_DIRS에 경로 저장됨

catkin_package( # 패키지의 정보를 다른 패키지들에 export 하기 위한 용도로 사용 
  # INCLUDE_DIRS include : 생성된 헤더 파일들이 위치하는 디렉토리
  # LIBRARIES $ {PROJECT_NAME} : 프로젝트에 해당되는 라이브러리들이 위치하는 디렉토리
  # CATKIN_DEPENDS roscpp rospy cv_bridge std_msgs sensor_msgs image_transport : 프로젝트의 catkin 의존성 패키지들
  # DEPENDS opencv : catkin에 포함되지 않은 의존성 패키지들
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(laneDetect src/laneDetect.cpp)
target_link_libraries(laneDetect
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
)

add_executable(saveImage src/saveImage.cpp)
target_link_libraries(saveImage
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
)
