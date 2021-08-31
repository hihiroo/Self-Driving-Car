# The Client

Clients는 CARLA 구조의 주요 요소 중 하나이다. 이것을 이용하여 user는 서버에 연결하고 시뮬레이션에서부터 명령의 변경, 정보 회수까지 할 수 있다. 이는 Client가 자신을 식별하고 시뮬레이션과 함께 작동하기위해 world에 연결하는 스크립트를 통해 이루어진다.

이 외에도 Client는 CARLA 모듈, 기능에 접근하고 명령 배치를 적용할 수 있다. 명령 배치는 actor의 스폰이 요구되는 즉시 필요하므로 지금부터의 설명과 연관이 있다. 나머지는 더 복잡한 내용이기 때문에 이 부분에서는 아직 다루지 않는다. **carla.Client** 클래스는 **[PythonAPI reference](https://carla.readthedocs.io/en/0.9.8/python_api/#carla.Client)**에서 자세히 설명된다.

## Client creation (Client 생성)

---

Client를 식별할 IP와 서버와 통신하기 위한 2개의 TCP포트가 필요하다. 

```python
client = carla.Client('localhost', 2000)
```

세 번째 파라미터는 선택인데, working thread를 설정하는 정수 값이다. 기본으로 all(0)이다. 

기본적으로 CARLA는 로컬호스트와 2000번 포트를 연결에 사용하지만 바꿀 수 있다. 두번째 포트는 항상 n+1번 포트를 사용한다. (이 경우 2001번)

스크립트를 실행할 때의 arguments를 파싱하여 설정하는 방법은 다음과 같다.

```python
argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-s', '--speed',
        metavar='FACTOR',
        default=1.0,
        type=float,
        help='rate at which the weather changes (default: 1.0)')
    args = argparser.parse_args()

    speed_factor = args.speed
    update_freq = 0.1 / speed_factor

    client = carla.Client(args.host, args.port)
```

Client가 생성되면 시간초과를 설정한다. 이것은 모든 네트워킹 작업에 제한을 두면서 Client가 영구적으로 차단되지 않도록 연결에 실패하면 오류를 반환하게 해준다.

```python
client.set_timeout(10.0) # seconds
```

일반적으로 한 번에 여러 개의 스크립트를 실행해야되기 때문에 한 번에 여러 Client들을 연결할 수 있다. 주의할 점은 traffic manager나 동기화 모드같은 고급 CARLA 기능을 실행하며 다중 클라이언트를 연결하게 되면 통신이 더 복잡해진다.

클라이언트와 서버의 libcarla 모듈이 다르기 때문에 버전이 서로 다르면 문제가 발생할 수 있다. 일반적으로 발생하는 일은 아니지만 get_client_version(), get_server_version() 메서드를 사용하여 확인할 수 있다.

## World Connection (world에 연결)

---

시뮬레이션이 실행되고 있는 동안, 정의된 클라이언트는 현재 world에 쉽게 연결하고 회수할 수 있다.

```python
world = client.get_world()
```

`reload_world()` 를 사용하여 client는 동일한 맵으로 world의 새 인스턴스를 만든다. 일종의 재부팅 방법이다. 클라이언트는 또한 현재 맵을 변경하는데 사용되는 맵 목록을 가져올 수도 있다. 이것은 현재의 world를 없애고 새로운 것을 만든다.

```python
print(client.get_available_maps())
... # 변경 가능한 맵 목록 출력됨
world = client.load_world('Town01') # 변경할 맵 선택하여 불러오기
```

모든 world 오브젝트들은 id와 에피소드를 가진다. 클라이언트가 `load_world()` 또는 `reload_word()` 를 호출할 때 마다 Unreal Engine을 재부팅 하는 것 없이 이전의 것은 파괴되고 새로운 항목이 생성되면서 에피소드가 변경된다.

## Other client utilities

---

클라이언트 객체의 주된 목적은 world를 얻거나 변경시키는 것이며, 그 이후에는 더 이상 사용되지 않는 경우가 많다. 그러나 이 오브젝트는 고급 CARLA 기능에 대한 액세스와 명령 배치 적용이라는 두 개의 다른 주요 작업을 담당한다. 클라이언트가 액세스하는 기능 목록은 다음과 같다.

- **Traffic manager** : 이 모듈은 자동운전으로 설정된 모든 차량을 담당한다.
- **Recorder** : 프레임당 시뮬레이션 상태를 요약하는 스냅샷을 이용하여 이전 시뮬레이션을 재현할 수 있다.

배치는 시뮬레이션의 동일한 단계에서 일괄적으로 실행되도록 준비된 일반적인 함수이다. 다음 예제는 vehicle_list에 포함된 모든 차량을 한 번에 파괴한다.

```python
client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])
```

`apply_batch_sync()` 메서드는 오직 동기 모드에서만 사용할 수 있으며 적용된 명령마다 command.Response를 반환한다.