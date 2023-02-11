from interfaces.command import Command
import ioc.container


class ScopeNew(Command):
    def __init__(self, parent: int):
        self._parent = parent

    def execute(self) -> None:
        ioc.container.IoC.scopes.new_scope(parent=self._parent)


class ScopeSetCurrent(Command):
    def __init__(self, scope: int):
        self._scope = scope

    def execute(self) -> None:
        ioc.container.IoC.scopes.current_scope = self._scope
