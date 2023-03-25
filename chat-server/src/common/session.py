import asyncio
import json
from dataclasses import dataclass, field
from websockets.server import WebSocketServerProtocol
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed

from typing import TypedDict
from collections.abc import Callable, Awaitable


class SessionHandler(TypedDict):
    on_connect: Callable[['Session'], Awaitable]
    on_disconnect: Callable[['Session'], Awaitable]
    on_recv_msg: Callable[['Session', dict], Awaitable]


@dataclass
class Session:
    user_name: str = field(init=False, default=None)
    future: asyncio.Future = field(init=False, default=None)
    websocket: WebSocketServerProtocol | WebSocketClientProtocol
    handler: SessionHandler = field(init=False, default=None)
    room_id: int = field(init=False, default=None)

    def set_recv_handler(self, handler):
        self.handler['on_recv_msg'] = handler

    async def start(self, handler: SessionHandler) -> None:
        self.handler = handler
        try:
            asyncio.create_task(self.handler['on_connect'](self))
            while msg := await self.recv_msg():
                await self.handler['on_recv_msg'](self, msg)
        except ConnectionClosed:
            print("Remote disconnected")
        finally:
            await self.handler['on_disconnect'](self)


    async def recv_msg(self) -> dict:
        return json.loads(await self.websocket.recv())

    async def send_msg(self, msg: dict) -> None:
        await self.websocket.send(json.dumps(msg))

    async def create_future(self):
        loop = asyncio.get_running_loop()
        self.future = loop.create_future()

    async def wait_for_future(self) -> dict:
        return await self.future

    def set_result_future(self, msg: dict) -> None:
        self.future.set_result(msg)
