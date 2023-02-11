import threading

from commands.scope import ScopeNew, ScopeSetCurrent
from ioc.container import Register


class Scopes(threading.local):

    class _Scope:
        def __init__(self, index: int, parent: int | None):
            self.parent = parent
            self.id = index

    def __init__(self):
        super().__init__()
        root_scope = self._Scope(index=0, parent=None)  # create root scope
        root_scope.__setattr__('IoC.Register', Register)
        root_scope.__setattr__('Scope.New', ScopeNew)
        root_scope.__setattr__('Scope.SetCurrent', ScopeSetCurrent)
        self.value: dict = {0: root_scope}  # set root scope
        self._max_scope_id: int = 0
        self._cur_scope: int = 0

    @property
    def current_scope(self) -> _Scope:
        return self.value[self._cur_scope]

    @current_scope.setter
    def current_scope(self, index: int) -> None:
        self._cur_scope = index

    def new_scope(self, parent: int | None):
        self._max_scope_id += 1
        new_scope = self._Scope(index=self._max_scope_id, parent=parent)
        self.value.update({self._max_scope_id: new_scope})
        self._cur_scope = self._max_scope_id

    # def get_scope_by_id(self, index: int) -> _Scope:
    #     return self.value[index]
