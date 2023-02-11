from Interfaces.command import Command
from Interfaces.fuel import Fuelable


class BurnFuel(Command):
    def __init__(self, f: Fuelable):
        self._f = f

    def execute(self):
        self._f.fuel = self._f.fuel - self._f.fuel_rate
