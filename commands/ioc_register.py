from interfaces.command import Command
from ioc.container import IoC


class Register(Command):
    """
    IoC.Register
    register dependencies in ioc container
    """
    def __init__(self, key: str, func: callable):
        self._key = key
        self._func = func

    def execute(self) -> None:
        IoC._register(self._key, self._func)
