from dataclasses import dataclass


@dataclass
class CommandInfo:
    object_id: int
    operation_id: int
    args: dict


@dataclass
class Message:
    game_id: int
    command_info: CommandInfo
