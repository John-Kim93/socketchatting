from dataclasses import dataclass, field


@dataclass
class ChatRoom:
    room_id: int = None
    room_name: str = None
    creater_name: str = None
    sessions: list["ClientSession"] = field(default_factory=list)

    def enter(self, session: "ClientSession"):
        self.sessions.append(session)
        session.room = self

    def leave(self, session: "ClientSession"):
        self.sessions.remove(session)
        session.room = None
