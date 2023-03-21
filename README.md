# socketchatting
#### 사용 방법

클라이언트 실행 : Client_user/client-user에서 npm start 입력

테스트 서버 실행 : node_test_server에서 npm i ws 이후 node WebSocketEchoServer.js 입력

파이썬 서버 실행 : cd py-server 에서 pdm run app.py



#### version 관리

1.0.0 - 중대한 변화가 있는 경우

1.1.0 - 고도화 작업 완료 시

1.1.1 - 유의미한 기능 변화가 있을 시

버그 수정은 version_hotfix로 간단하게 처리

초기 버전 기능 추가에 따른 버전 업그레이드는 불필요



#### Protocol

1. 방 생성

   - send

     - type : ROOM_CREATE(01)

     - roomName : string(max length = 30)

     - userName : string(max length = 10)

   - receive

     - status : bool (true = "success" / false = "fail")
     - roomID : number(int)
     - message : "{userName}님이 참여하였습니다."

2. 방 삭제

   - send

     - type : ROOM_DELETE(02)

     - roomID : number(int)
     - userName : string(max length = 10)

   - receive

     - status : bool (true = "success" / false = "fail")

3. 방 참여

   - send

     - type : ROOM_JOIN(03)

     - roomID : number(int)

     - userName : string(max length = 10)

   - receive

     - status : bool (true = "success" / false = "fail")
     - roomID : number(int)
     - message : "{userName}님이 참여하였습니다."

4. 방 퇴장

    - send

      - type : ROOM_EXIT(04)

      - roomID : number(int)

      - userName : string(max length = 10)

    - receive

      - status : bool (true = "success" / false = "fail")
      - roomID : number(int)
      - message : "{userName}님이 참여하였습니다."

5. 채팅 입력

    - send

      - type : CHAT_SEND(10)

      - roomID : number(int)

      - userName : string(max length = 10)
      - message : string(max length = 128)

    - receive

      - status : bool (true = "success" / false = "fail")
      - roomID : number(int)
      - nickname : string(max length = 10)
      - message : string(max length = 128)



#### conditions

- 방 생성 시 자동 입장(방장)
- 방장이 방 퇴장 시 방 삭제
- 방 삭제 시 방장인지 확인
