from abc import ABC, abstractmethod
from typing import Any

__all__ = ['UObject']


class UObject(ABC):

    @abstractmethod
    def get_property(self, name: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set_property(self, name: str, value: Any) -> None:
        raise NotImplementedError
