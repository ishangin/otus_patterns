from Interfaces.command import Command


class ScopeNew(Command):
    def __init__(self, scopes: object, parent: int):
        self._scopes = scopes
        self._parent = parent

    def execute(self) -> None:
        self._scopes.new_scope(parent=self._parent)


class ScopeSetCurrent(Command):
    def __init__(self, scopes: object, scope: int):
        self._scopes = scopes
        self._scope = scope

    def execute(self) -> None:
        self._scopes.current_scope = self._scope
