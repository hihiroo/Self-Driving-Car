# launch 파일 작성법

참고 : https://enssionaut.com/board_robotics/974 <br>
https://swimminglab.tistory.com/95

**&#60;launch>** : launch 파일을 시작한다. launch 파일은 &#60;launch> 태그로 시작하여 &#60;/launch> 태그로 종료된다.

**&#60;include>** : 다른 launch 파일을 가져온다.

**&#60;arg>** : launch 파일 내부에서 변수처럼 사용될 수 있도록 값을 정의한다. include하는 launch 파일의 arg도 설정할 수 있다.  
```xml
<include file="$(find carla_ros_bridge)/launch/carla_ros_bridge.launch">
    <arg name='host' value='$(arg host)'/>
</include>
```

**&#60;node>** : 노드를 실행시킨다.  
> pkg - 노드가 포함되어 있는 패키지  
> type - 실행 파일  
> name - 노드 이름 지정  
> output - 값이 screen이면 화면에 결과를 출력하고 log이면 로그 파일을 $ROS_HOME/log 경로에 생성한다.

**&#60;param>** : 노드에서 사용되는 파라미터(글로벌 변수)의 값을 설정한다.