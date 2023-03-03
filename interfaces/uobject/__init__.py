from typing import Any

__all__ = ['UObject']


class UObject:

    def get_property(self, name: str) -> Any:
        return self.__getattribute__(name)

    def set_property(self, name: str, value: Any) -> None:
        self.__setattr__(name, value)
