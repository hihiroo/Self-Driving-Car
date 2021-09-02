# carla_ros_bridge 패키지 분석

### **launch 파일**
1. **carla_ros_bridge.launch**
    * 실행파일 : bridge.py  
        > 노드이름 : carla_ros_bridge  
        > 파라미터 : rosbag_fname, carla/host, carla/port, carla/synchronous_mode, carla/synchronous_mode_wait_for_vehicle_control_command, carla/fixed_delta_seconds, carla/town

2. **carla_ros_bridge_with_example_ego_vehicle.launch**
   * 실행파일 : carla_ros_bridge/launch/carla_ros_bridge.launch
        > 파라미터 : host, port, town, synchronous_mode, synchronous_mode_wait_for_vehicle_control_command, fixed_delta_seconds

   * 실행파일 : carla_ego_vehicle/launch/carla_example_ego_vehicle.launch
        > 파라미터 : host, port, vehicle_filter, role_name, spawn_point

   * 실행파일 : carla_manual_control/launch/carla_manual_control.launch
        > 파라미터 : role_name

### **python 파일**
1. **bridge.py** : 동기모드인 경우 CarlaControl 타입의 "/carla/control" 토픽들을 subscribe하고 Pause, Play로 실행을 컨트롤할 수 있음. 또 하나씩 명령을 수행하도록 할 수도 있음. 전체적으로 actor를 생성하고 actor 데이터 토픽들을 publish하는 기능 수행.
