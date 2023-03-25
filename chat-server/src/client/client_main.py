import asyncio
import websockets
import random
from dataclasses import dataclass, field

from ..common import Session


async def ainput(prompt: str):
    return await asyncio.to_thread(input, prompt)


def get_random_sentance():
    chars = "abcdefghijklmnopqrstuvxyz1234567890 "
    return "".join([chars[random.randrange(0, len(chars))]
                    for _ in range(random.randrange(5, 20))])


@dataclass
class ClientMain:
    host: str = field(default="localhost")
    port: int = field(default=8100)
    url: str = field(init=False)

    def __post_init__(self):
        self.url = f"ws://{self.host}:{self.port}"

    async def start(self):
        async with websockets.connect(self.url) as websocket:
            await Session(websocket).start({
                "on_connect": self.on_connect,
                "on_disconnect": self.on_disconnect,
                "on_recv_msg": self.on_recv_msg
            })

    async def on_connect(self, session: Session):
        user_name = await self.input_username()

        await self.sr_client_name_set(session, user_name)


        if await self.input_select_action():
            room_name = await self.input_room_name()
            await self.sr_client_room_create(session, room_name)
        else:
            room_list = await self.sr_client_room_list(session)
            room_id = await self.input_room_select(room_list)
            await self.sr_client_room_join(session, room_id)

        while True:
            await asyncio.sleep(random.randrange(1, 3))
            sentance = get_random_sentance()
            await self.send_client_chat_send(session, sentance)

    async def on_disconnect(self, session: Session):
        pass

    async def input_username(self) -> str:
        print("이름이 뭐세요?")
        return await ainput("> ")

    async def input_select_action(self):
        print("방을 생성 하시곘습니까? (Y/N)")
        answer = await ainput("> ")
        return answer == "Y"

    async def input_room_name(self):
        print("방 이름을 입력하세요.")
        return await ainput("> ")

    async def input_room_select(self, room_list):
        print("입장하실 방 번호를 입력하세요.")
        print("-" * 40)
        for r in room_list:
            print(f"{r['room_id']} {r['room_name']} {r['host']}")
        print("-" * 40)
        return int(await ainput("> "))


    async def sr_client_name_set(self, session: Session, user_name: str):
        await session.create_future()
        await session.send_msg({
            "type": "CLIENT_NAME_SET",
            "userName": user_name
        })
        await session.wait_for_future()

    async def sr_client_room_list(self, session: Session):
        await session.create_future()
        await session.send_msg({
            "type": "CLIENT_ROOM_GET"
        })
        msg = await session.wait_for_future()
        return msg["roomList"]

    async def sr_client_room_create(self, session: Session, room_name: str):
        await session.create_future()
        await session.send_msg({
            "type": "CLIENT_ROOM_CREATE",
            "roomName": room_name
        })
        await session.wait_for_future()

    async def sr_client_room_join(self, session: Session, room_id: int):
        await session.create_future()
        await session.send_msg({
            "type": "CLIENT_ROOM_JOIN",
            "roomId": room_id
        })
        await session.wait_for_future()


    async def send_client_chat_send(self, session: Session, chat: str):
        await session.send_msg({
            "type": "CLIENT_CHAT_SEND",
            "message": chat
        })

    async def on_recv_msg(self, session: Session, msg: dict):
        if msg["type"] == "SERVER_NAME_SET":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_ROOM_GET":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_ROOM_CREATE":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_ROOM_JOIN":
            session.set_result_future(msg)
        elif msg["type"] == "BROAD_ROOM_CREATE":
            print(f"room create: {msg['roomId']} {msg['roomName']}")
        elif msg["type"] == "BROAD_ROOM_JOIN":
            print(f"room join: {msg['nickName']}")
        elif msg["type"] == "BROAD_ROOM_EXIT":
            print(f"room exit: {msg['nickName']}")
        elif msg["type"] == "BROAD_CHAT_SEND":
            print(f"from {msg['nickName']}: {msg['message']}")
