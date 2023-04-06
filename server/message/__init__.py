from dataclasses import dataclass

from server.message.operation import OPERATION


@dataclass
class CommandInfo:
    object_id: int
    operation: OPERATION
    args: dict


@dataclass
class Message:
    game_id: int
    conn: int | None
    command_info: CommandInfo
