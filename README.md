# socketchatting

## 개요

소켓 통신을 활용한 채팅방 기능 구현

#### 사용 방법

클라이언트 실행 : Client_user/client-user에서 npm start 입력

테스트 서버 실행 : node_test_server에서 npm i ws 이후 node WebSocketEchoServer.js 입력

파이썬 서버 실행 : cd chat-server 에서 pdm run server

파이썬 클라 실행 : cd chat-server 에서 pdm run client



#### version 관리

1.0.0 - 중대한 변화가 있는 경우

1.1.0 - 고도화 작업 완료 시

1.1.1 - 유의미한 기능 변화가 있을 시

버그 수정은 version_hotfix로 간단하게 처리

초기 버전 기능 추가에 따른 버전 업그레이드는 불필요



#### Protocol

* send : 클라이언트에서 보내는 메시지 / unicast : 서버에서 unicast로 받은 메시지 / broadcast : 서버에서 broadcast로 받은 메시지
* type rule : ACTOR_DOMAIN_ACTION

0. 닉네임 설정

   - send
   
     - type : CLIENT_NAME_SET
     
     - userName : string(max length = 10)
   
   - unicast
   
     - type : SERVER_NAME_SET
     
     - status : bool (true = "success" / false = "fail")

1. 방 생성

   - send

     - type : CLIENT_ROOM_CREATE

     - roomName : string(max length = 30)

   - unicast

     - type : SERVER_ROOM_CREATE

     - status : bool (true = "success" / false = "fail")
     
   - broadcast
   
     - type : BROAD_ROOM_CREATE     
     
     - roomID : number(int)
     
     - roomName : string(max length = 30)

2. 방 조회

   - send

     - type : CLIENT_ROOM_GET

   - unicast
   
     - type : SERVER_ROOM_GET

     - status : bool (true = "success" / false = "fail")

     - roomList : [ { roomID : number(int), roomName : string(max length = 30), host : string(max length = 10) }, ... ]
     
       (TODO : roomList pagination 최적화)

   - broadcast
   
     - type : BROAD_ROOM_GET
     
     - roomList : [ { roomID : number(int), roomName : string(max length = 30), host : string(max length = 10) }, ... ]
     
3. 방 참여

   - send

     - type : CLIENT_ROOM_JOIN

     - roomID : number(int)

   - unicast
   
     - type : SERVER_ROOM_JOIN

     - status : bool (true = "success" / false = "fail")

     - roomID : number(int)

     - roomName : string(max length = 30)
     
       ( TODO : userList )
     
   - broadcast (~님이 입장하셨습니다.)
     
     - type : BROAD_ROOM_JOIN
     
     - nickName : string(max length = 10)

4. 방 퇴장

    - send

      - type : CLIENT_ROOM_EXIT

    - unicast
    
      - type : SERVER_ROOM_EXIT

      - status : bool (true = "success" / false = "fail")
      
    - broadcast

      - type : BROAD_ROOM_EXIT
      
      - nickName : string(max length = 10)

      - isHost : bool
      
5. 채팅 입력

    - send

      - type : CLIENT_CHAT_SEND

      - message : string(max length = 128)

    - broadcast
    
      - type : BROAD_CHAT_SEND

      - nickname : string(max length = 10)
      
      - message : string(max length = 128)


#### conditions

- 방 생성 성공 시 자동 입장(방장)
- 방장이 방 퇴장 시 방 삭제
- 방 삭제 시 방장인지 확인
