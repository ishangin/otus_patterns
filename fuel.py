from abc import ABC, abstractmethod

from command import Command
from errors import CommandException


__all__ = ['Fuelable', 'CheckFuel', 'BurnFuel']


class Fuelable(ABC):
    """ Fuel interface"""

    @property
    @abstractmethod
    def fuel(self) -> int:
        """ getter for fuel """
        ...

    @fuel.setter
    @abstractmethod
    def fuel(self, value: int) -> None:
        """ setter for fuel """
        ...

    @property
    @abstractmethod
    def fuel_rate(self) -> int:
        """ fuel rate per move """
        ...

    # @property
    # @abstractmethod
    # def max_fuel(self) -> int:
    #     """ max fuel capacity """
    #     ...


class CheckFuel(Command):
    def __init__(self, f: Fuelable):
        self._f = f

    def execute(self):
        if self._f.fuel >= self._f.fuel_rate:
            return
        else:
            raise CommandException('low fuel')


class BurnFuel(Command):
    def __init__(self, f: Fuelable):
        self._f = f

    def execute(self):
        self._f.fuel = self._f.fuel - self._f.fuel_rate
