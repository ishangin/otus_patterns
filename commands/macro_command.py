from Interfaces.command import Command
from errors.errors import CommandException
from main import log


class MacroCommand(Command):
    _commands = []

    def __init__(self, commands: list[Command]):
        self._commands = commands

    def execute(self):
        try:
            for command in self._commands:
                command.execute()
        except CommandException as ex:
            log.error(ex)
            raise
