import asyncio
import websockets
from dataclasses import dataclass, field

from ..common import Session


@dataclass
class ServerMain:
    host: str = field(default="localhost")
    port: int = field(default=8100)

    init_sessions: list[Session] = field(init=False, default_factory=list)
    chat_sessions: list[Session] = field(init=False, default_factory=list)

    async def start(self) -> None:
        async with websockets.serve(self.on_accept, self.host, self.port) as server:
            print(f"Listeneing on {self.host}:{self.port}")
            await server.serve_forever()

    async def on_accept(self, *args) -> None:
        session = Session(*args)

        self.init_sessions.append(session)
        await session.start({
            "on_connect": self.on_connect,
            "on_disconnect": self.on_disconnect,
            "on_recv_msg": self.on_recv_msg
        })

    async def on_connect(self, session: Session):
        pass

    async def on_disconnect(self, session: Session):
        pass

    async def on_recv_msg(self, session: Session, msg: dict):
        if msg["type"] == "CLIENT_NAME_SET":
            await self.on_recv_client_name_set(session, msg)
            await self.send_server_name_set(session)
        elif msg["type"] == "CLIENT_ROOM_LIST":
            await self.send_server_room_list(session)
        elif msg["type"] == "CLIENT_ROOM_CREATE":
            await self.send_server_room_create(session)
        elif msg["type"] == "CLIENT_CHAT_SEND":
            await self.send_server_chat_send(session, msg["chat"])

    async def on_recv_client_name_set(self, session: Session, msg: dict):
        session.user_name = msg["userName"]
        self.init_sessions.remove(session)
        self.chat_sessions.append(session)

    async def send_server_name_set(self, session: Session):
        await session.send_msg({"type": "SERVER_NAME_SET", "status": True})

    async def send_server_room_list(self, session: Session):
        await session.send_msg({"type": "SERVER_ROOM_LIST"})

    async def send_server_room_create(self, session: Session):
        await session.send_msg({"type": "SERVER_ROOM_CREATE", "status": True})

    async def send_server_chat_send(self, session: Session, chat: str):
        msg = {"type": "SERVER_CHAT_SEND",
               "userName": session.user_name, "chat": chat}
        await asyncio.gather(*[s.send_msg(msg) for s in self.chat_sessions])
