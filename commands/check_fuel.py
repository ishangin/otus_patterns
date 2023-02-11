from interfaces.command import Command
from interfaces.fuel import Fuelable
from errors.errors import CommandException


class CheckFuel(Command):
    def __init__(self, f: Fuelable):
        self._f = f

    def execute(self):
        if self._f.fuel >= self._f.fuel_rate:
            return
        else:
            raise CommandException('low fuel')
