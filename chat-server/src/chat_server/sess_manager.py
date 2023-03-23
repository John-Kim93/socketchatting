from dataclasses import dataclass, field
from .room_manager import RoomManager
from .client_session import ClientSession


@dataclass
class SessManager:
    user_names: dict[str, None] = field(default_factory=dict)
    all_sessions: list[ClientSession] = field(default_factory=list)
    lobby_sessions: list[ClientSession] = field(default_factory=list)
    room_mgr = RoomManager()

    async def generate(self, websocket):
        session = ClientSession(
            websocket=websocket,
            on_connect=self.on_connect,
            on_disconnect=self.on_disconnect,
            on_recv_msg=self.on_recv_msg
        )
        self.all_sessions.append(session)
        self.lobby_sessions.append(session)

        await session.start()

        if not session.room:
            self.lobby_sessions.remove(session)
        else:
            session.room.leave(session)
        self.all_sessions.remove(session)

    async def on_connect(self, session: ClientSession):
        print("on connect")

    async def on_disconnect(self, session: ClientSession):
        print("on disconnect")

    async def broadcast_lobby_sessions(self, msg: dict):
        for s in self.lobby_sessions:
            await s.send(msg)

    async def on_recv_msg(self, session: ClientSession, msg: dict):
        funcs = {
            "CLIENT_NAME_SET": self.on_client_name_set,
            "CLIENT_ROOM_CREATE": self.on_client_room_create,
            "CLIENT_ROOM_DELETE": self.on_client_room_delete,
            "CLIENT_ROOM_JOIN": self.on_client_room_join,
            "CLIENT_ROOM_EXIT": self.on_client_room_exit,
            "CLIENT_CHAT_SEND": self.on_client_chat_send,
        }
        await funcs[msg["type"]](session, msg)

    async def on_client_name_set(self, session: ClientSession, msg: dict):
        status = True
        if not self.user_names.get(msg["userName"]):
            self.user_names.setdefault(msg["userName"])
        else:
            status = False

        await session.send({"type": "SERVER_NAME_SET", "status": status})

    async def on_client_room_create(self, session: ClientSession, msg: dict):
        room = self.room_mgr.create_room(msg["roomName"], session.user_name)

        self.lobby_sessions.remove(session)
        room.enter(session)

        await session.send({"type": "SERVER_ROOM_CREATE", "room_id": room.room_id})

        await self.broadcast_lobby_sessions({
            "type": "BROAD_ROOM_CREATE", "room_id": room.room_id, "room_name": room.room_name})

    async def on_client_room_delete(self, session: ClientSession, msg: dict):
        pass

    async def on_client_room_join(self, session: ClientSession, msg: dict):
        pass

    async def on_client_room_exit(self, session: ClientSession, msg: dict):
        pass

    async def on_client_chat_send(self, session: ClientSession, msg: dict):
        pass
