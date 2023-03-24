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
        print("Enter the name you want to use.")
        user_name = await ainput("> ")

        await self.sr_client_name_set(session, user_name)

        await self.sr_client_room_list(session)

        await self.sr_client_room_create(session, "My Room #1")

        while True:
            await asyncio.sleep(random.randrange(1, 3))
            sentance = get_random_sentance()
            await self.send_client_chat_send(session, sentance)

    async def on_disconnect(self, session: Session):
        pass

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
            "type": "CLIENT_ROOM_LIST"
        })
        await session.wait_for_future()

    async def sr_client_room_create(self, session: Session, room_name: str):
        await session.create_future()
        await session.send_msg({
            "type": "CLIENT_ROOM_CREATE",
            "roomName": room_name
        })
        await session.wait_for_future()

    async def send_client_chat_send(self, session: Session, chat: str):
        await session.send_msg({
            "type": "CLIENT_CHAT_SEND",
            "chat": chat
        })

    async def on_recv_msg(self, session: Session, msg: dict):
        if msg["type"] == "SERVER_NAME_SET":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_ROOM_LIST":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_ROOM_CREATE":
            session.set_result_future(msg)
        elif msg["type"] == "SERVER_CHAT_SEND":
            print(f"from {msg['userName']}: {msg['chat']}")
