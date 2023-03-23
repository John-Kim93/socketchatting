import asyncio
import websockets
from dataclasses import dataclass
from ..server_core import WSSession


@dataclass
class ClientMain:
    uri = "ws://localhost:8100"

    def start(self):
        try:
            asyncio.run(self.connect(1))
        except KeyboardInterrupt:
            pass

    async def connect(self, count: int):
        tasks = []
        for _ in range(count):
            tasks.append(asyncio.create_task(self.connect_one()))

        await asyncio.wait(tasks)

    async def connect_one(self):
        websocket = await websockets.connect(self.uri)
        session = WSSession(
            websocket=websocket,
            on_connect=self.on_connect,
            on_disconnect=self.on_disconnect,
            on_recv_msg=self.on_recv_msg
        )
        await session.start()

    async def on_connect(self, session: WSSession):
        print(f"on_connect")
        asyncio.create_task(self.test_main(session))

    async def on_disconnect(self, session: WSSession):
        print(f"on_disconnect")

    async def on_recv_msg(self, session: WSSession, msg: dict):
        funcs = {
            "SERVER_NAME_SET": self.on_server_name_set,
            "SERVER_ROOM_CREATE": self.on_server_room_create,
            "BROAD_ROOM_CREATE": self.on_broad_room_create,
            "SERVER_ROOM_DELETE": self.on_server_room_delete,
            "BROAD_ROOM_DELETE": self.on_broad_room_delete,
            "SERVER_ROOM_JOIN": self.on_server_room_join,
            "BROAD_ROOM_JOIN": self.on_broad_room_join,
            "SERVER_ROOM_EXIT": self.on_server_room_exit,
            "BROAD_ROOM_EXIT": self.on_broad_room_exit,
            "BROAD_CHAT_SEND": self.on_broad_chat_send,
        }
        await funcs[msg["type"]](session, msg)

    async def acquire_waiter(self):
        self.future = asyncio.get_running_loop().create_future()
        return await self.future

    def release_waiter(self, result):
        self.future.set_result(result)

    async def on_server_name_set(self, session: WSSession, msg: dict):
        self.release_waiter(msg["status"])

    async def on_server_room_create(self, session: WSSession, msg: dict):
        self.release_waiter(msg["room_id"])

    async def on_broad_room_create(self, session: WSSession, msg: dict):
        print(f"{msg['room_name']}({msg['room_in']}) room created")

    async def on_server_room_delete(self, session: WSSession, msg: dict):
        pass

    async def on_broad_room_delete(self, session: WSSession, msg: dict):
        pass

    async def on_server_room_join(self, session: WSSession, msg: dict):
        pass

    async def on_broad_room_join(self, session: WSSession, msg: dict):
        pass

    async def on_server_room_exit(self, session: WSSession, msg: dict):
        pass

    async def on_broad_room_exit(self, session: WSSession, msg: dict):
        pass

    async def on_broad_chat_send(self, session: WSSession, msg: dict):
        pass

    async def send_client_name_set(self, session: WSSession, user_name: str):
        await session.send({"type": "CLIENT_NAME_SET", "userName": user_name})
        return await self.acquire_waiter()

    async def send_client_room_create(self, session: WSSession, room_name: str):
        await session.send({"type": "CLIENT_ROOM_CREATE", "roomName": room_name})
        return await self.acquire_waiter()

    async def send_client_room_delete(self, session: WSSession, room_id: int):
        await session.send({"type": "CLIENT_ROOM_DELETE", "roomId": room_id})
        return await self.acquire_waiter()

    async def test_main(self, session: WSSession):
        user_name, room_name = "Bot#1", "Room#1"
        _ = await self.send_client_name_set(session, user_name)
        room_id = await self.send_client_room_create(session, room_name)
        print(f"{user_name} enters room {room_name}({room_id})")

        while True:
            await asyncio.sleep(1.0)
