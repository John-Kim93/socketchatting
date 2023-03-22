
from dataclasses import dataclass, field
from ..server_core import WSSession


@dataclass
class SessManager:
    sessions: list[WSSession] = field(default_factory=list)
    user_names: dict[str, None] = field(default_factory=dict)

    async def generate(self, websocket):
        session = WSSession(
            websocket=websocket,
            on_connect=self.on_connect,
            on_disconnect=self.on_disconnect,
            on_recv_msg=self.on_recv_msg
        )
        self.sessions.append(session)
        await session.start()
        self.sessions.remove(session)

    async def on_connect(self, session: WSSession):
        pass

    async def on_disconnect(self, session: WSSession):
        pass

    async def on_recv_msg(self, session: WSSession, msg: dict):
        if msg["type"] == "CLIENT_NAME_SET":
            await self.on_recv_client_name_set(session, msg)

    async def on_recv_client_name_set(self, session: WSSession, msg: dict):
        status = True
        if not self.user_names.get(msg["userName"]):
            self.user_names.setdefault(msg["userName"])
        else:
            status = False

        await session.send({"type": "SERVER_NAME_SET", "status": status})
