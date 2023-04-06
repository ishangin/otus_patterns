from queue import Queue

from interfaces.command import Command
from ioc.container import IoC
from server.message import CommandInfo
from server.message.operation import OPERATION


class InterpretCommand(Command):
    def __init__(self, queue: Queue, command_info: CommandInfo):
        self._queue = queue
        self._command_info = command_info

    def execute(self):
        params = [
            IoC.resolve('GameObjects'),
            *self._command_info.args.values()  # FIXME: think about message format args is JSON but keys not used
        ]
        self._queue.put(
            IoC.resolve(
                OPERATION(self._command_info.operation).name.replace('_', '.'),
                *params
            )
        )
