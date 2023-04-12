from dataclasses import dataclass, field
from .chatting_room import ChattingRoom
from ..common import Session


@dataclass
class RoomManager:
    last_id: int = 0
    rooms: dict[int, ChattingRoom] = field(default_factory=dict)

    def create_room(self, room_name: str, host_name:  str):
        self.last_id += 1
        room_id = self.last_id

        room = ChattingRoom(room_id, room_name, host_name)
        self.rooms[room_id] = room

        return room_id

    def join_room(self, room_id: int, session: Session):
        room = self.rooms[room_id]
        room.join_room(session)
        session.room_id = room_id

    def exit_room(self, session: Session):
        room = self.rooms[session.room_id]
        room.exit_room(session)
        if self.is_host(session):
            del self.rooms[session.room_id]
        session.room_id = None

    def is_host(self, session: Session):
        room = self.rooms[session.room_id]
        return room.host_name == session.user_name

    def get_room_list(self):
        room_list = []
        for r in self.rooms.values():
            room_list.append(
                {"room_id": r.room_id, "room_name": r.room_name, "host": r.host_name})
        return room_list

    async def broadcast(self, room_id: int, msg: dict):
        await self.rooms[room_id].broadcast(msg)
