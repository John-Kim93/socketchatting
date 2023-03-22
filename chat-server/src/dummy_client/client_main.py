import asyncio
import websockets
from dataclasses import dataclass
from ..server_core import WSSession


@dataclass
class ClientMain:
    uri = "ws://localhost:8100"

    def start(self):
        try:
            asyncio.run(self.connect(10))
        except KeyboardInterrupt:
            pass

    async def connect(self, count: int):
        async with websockets.connect(self.uri) as websocket:
            session = WSSession(
                websocket=websocket,
                on_connect=self.on_connect,
                on_disconnect=self.on_disconnect,
                on_recv_msg=self.on_recv_msg
            )
            await session.start()

    async def on_connect(self, session: WSSession):
        print(f"on_connect")
        asyncio.create_task(self.main_loop(session))

    async def on_disconnect(self, session: WSSession):
        print(f"on_disconnect")

    async def on_recv_msg(self, session: WSSession, msg: dict):
        if msg["type"] == "SERVER_NAME_SET":
            await self.on_recv_server_name_set(session, msg)

    async def on_recv_server_name_set(self, session: WSSession, msg: dict):
        print(msg)

    async def main_loop(self, session: WSSession):
        await session.send({"type": "CLIENT_NAME_SET", "userName": "Lee"})
