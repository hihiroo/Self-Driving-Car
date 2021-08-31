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