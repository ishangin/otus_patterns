from abc import ABC, abstractmethod

__all__ = ["Fuelable"]


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
