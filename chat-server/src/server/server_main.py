import asyncio
import websockets
from dataclasses import dataclass, field
from ..common import Session
from .room_manager import RoomManager


@dataclass
class ServerMain:
    host: str = field(default="localhost")
    port: int = field(default=8100)

    sessions: list[Session] = field(init=False, default_factory=list)

    room_mgr: RoomManager = field(init=False, default_factory=RoomManager)

    async def start(self) -> None:
        async with websockets.serve(self.on_accept, self.host, self.port) as server:
            print(f"Listeneing on {self.host}:{self.port}")
            await server.serve_forever()

    async def on_accept(self, *args) -> None:
        session = Session(*args)

        self.sessions.append(session)
        await session.start({
            "on_connect": self.on_connect,
            "on_disconnect": self.on_disconnect,
            "on_recv_msg": self.on_recv_msg
        })
        self.sessions.remove(session)

    async def on_connect(self, session: Session):
        pass

    async def on_disconnect(self, session: Session):
        if session.room_id:
            self.room_mgr.exit_room(session)

    async def on_recv_msg(self, session: Session, msg: dict):
        if msg["type"] == "CLIENT_NAME_SET":
            await self.on_recv_client_name_set(session, msg)
            await self.send_server_name_set(session)
        elif msg["type"] == "CLIENT_ROOM_GET":
            await self.send_server_room_list(session)
        elif msg["type"] == "CLIENT_ROOM_CREATE":
            await self.on_recv_client_room_create(session, msg)
        elif msg["type"] == "CLIENT_ROOM_JOIN":
            await self.on_recv_client_room_join(session, msg)
        elif msg["type"] == "CLIENT_ROOM_EXIT":
            await self.on_recv_client_room_exit(session, msg)
        elif msg["type"] == "CLIENT_CHAT_SEND":
            await self.on_recv_client_chat_send(session, msg)

    async def on_recv_client_name_set(self, session: Session, msg: dict):
        session.user_name = msg["userName"]

    async def on_recv_client_room_create(self, session: Session, msg: dict):
        room_id = self.room_mgr.create_room(msg["roomName"], session.user_name)
        self.room_mgr.join_room(room_id, session)
        await session.send_msg({"type": "SERVER_ROOM_CREATE",
                                "status": True, "roomId": room_id})
        await self.braodcast({
            "type": "BROAD_ROOM_CREATE",
            "roomId": room_id, "roomName": msg["roomName"]
        })

    async def on_recv_client_room_join(self, session: Session, msg: dict):
        self.room_mgr.join_room(msg["roomId"], session)
        await session.send_msg({"type": "SERVER_ROOM_JOIN", "status": True})
        await self.room_mgr.broadcast(msg["roomId"], {
            "type": "BROAD_ROOM_JOIN", "nickName": session.user_name
        })

    async def on_recv_client_room_exit(self, session: Session, msg: dict):
        is_host = self.room_mgr.is_host(session)
        self.room_mgr.exit_room(session)
        await session.send_msg({"type": "SERVER_ROOM_EXIT", "status": True})
        await self.room_mgr.broadcast(msg["roomId"], {
            "type": "BROAD_ROOM_EXIT",
            "nickName": session.user_name,
            "isHost": is_host
        })

    async def on_recv_client_chat_send(self, session: Session, msg: dict):
        await self.room_mgr.broadcast(session.room_id, {
            "type": "BROAD_CHAT_SEND", "nickName": session.user_name,
            "message": msg["message"]
        })

    async def send_server_name_set(self, session: Session):
        await session.send_msg({"type": "SERVER_NAME_SET", "status": True})

    async def send_server_room_list(self, session: Session):
        room_list = self.room_mgr.get_room_list()
        await session.send_msg({"type": "SERVER_ROOM_GET", "status": True, "roomList": room_list})

    async def braodcast(self, msg: dict):
        await asyncio.gather(*[s.send_msg(msg) for s in self.sessions if not s.room_id])
