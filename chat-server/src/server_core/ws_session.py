import json
from dataclasses import dataclass
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed
from collections.abc import Callable, Awaitable


@dataclass
class WSSession:
    websocket: WebSocketServerProtocol
    user_name: str = None

    on_connect: Callable[["WSSession"], Awaitable] = None
    on_disconnect: Callable[["WSSession"], Awaitable] = None
    on_recv_msg: Callable[["WSSession"], Awaitable] = None

    async def start(self):
        try:
            await self.on_connect(self)

            while msg := await self.recv():
                await self.on_recv_msg(self, msg)
        except ConnectionClosed:
            print("connection closed")
        finally:
            await self.websocket.close()
            await self.websocket.wait_closed()
            await self.on_disconnect(self)

    async def recv(self) -> dict:
        return json.loads(await self.websocket.recv())

    async def send(self, msg: dict):
        await self.websocket.send(json.dumps(msg))
