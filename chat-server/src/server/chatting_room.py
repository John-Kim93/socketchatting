import asyncio
from dataclasses import dataclass, field
from ..common import Session

@dataclass
class ChattingRoom:
    room_id: int
    room_name: str
    host_name: str

    sessions: list[Session] = field(init=False, default_factory=list)

    def join_room(self, session: Session):
        self.sessions.append(session)

    def exit_room(self, session: Session):
        self.sessions.remove(session)

    async def broadcast(self, msg: dict):
        await asyncio.gather(*[s.send_msg(msg) for s in self.sessions])