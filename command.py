from abc import ABC, abstractmethod


class Command(ABC):
    """ command interface """

    @abstractmethod
    def execute(self) -> None:
        ...
