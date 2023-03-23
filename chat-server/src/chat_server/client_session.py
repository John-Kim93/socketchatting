from dataclasses import dataclass, field
from .chat_room import ChatRoom
from ..server_core import WSSession


@dataclass
class ClientSession(WSSession):
    room: ChatRoom = None
