from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    NEW_GAME = 0
    AUTH = 1
    GET_JWT = 2
    RESPONSE = 3


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


@dataclass
class Message:
    type: int
    data: dict
