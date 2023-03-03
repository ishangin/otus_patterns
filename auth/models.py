from dataclasses import dataclass
from enum import Enum
from queue import Queue


class MessageType(Enum):
    GET_JWT: int = 12
    RESPONSE: int = 13


@dataclass
class User:
    login: str
    password: str | None = None
    id: int | None = None
    authenticated: bool = False


@dataclass
class Game:
    id: int
    players: list
    tokens: list
    queue: Queue


@dataclass
class Message:
    type: MessageType
    data: dict
