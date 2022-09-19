from abc import ABC, abstractmethod

from interfaces.command import Command


class State(ABC):
    """ State pattern interface. command processing modes. """

    @abstractmethod
    def execute(self, cmd: Command) -> None:
        pass
