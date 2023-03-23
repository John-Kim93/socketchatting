from dataclasses import dataclass, field
from .chat_room import ChatRoom


@dataclass
class RoomManager:
    last_room_id: int = 0
    chat_rooms: list[ChatRoom] = field(default_factory=list)

    def create_room(self, room_name: str, user_name: str):
        self.last_room_id += 1
        room = ChatRoom(
            room_id=self.last_room_id, room_name=room_name, creater_name=user_name)
        self.chat_rooms.append(room)
        return room
