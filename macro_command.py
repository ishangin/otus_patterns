import logging

from command import Command
from mixed_types import MF, MRF
from errors import CommandException

from fuel import BurnFuel, CheckFuel
from move import Move
from rotate import Rotate, ChangeVelocity

__all__ = ["MacroCommand", "Movement"]

log = logging.getLogger(__name__)


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


class Movement(MacroCommand):
    def __init__(self, obj: MF):
        super().__init__([CheckFuel(obj), Move(obj), BurnFuel(obj)])


class Rotatement(MacroCommand):
    def __init__(self, obj: MRF):
        super().__init__([CheckFuel(obj), Rotate(obj), BurnFuel(obj), ChangeVelocity(obj)])
