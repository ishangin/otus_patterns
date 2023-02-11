import threading
from typing import TypeVar

from interfaces.command import Command
from commands.scope import ScopeNew, ScopeSetCurrent
from errors.errors import IocResolveException

T = TypeVar('T')


class Register(Command):
    """
    IoC.Register
    register dependencies in ioc container
    """
    def __init__(self, key: str, func: callable):
        self._key = key
        self._func = func

    def execute(self) -> None:
        IoC.scopes.current_scope.__setattr__(self._key, self._func)
        # IoC._register(self._key, self._func)


class Scopes(threading.local):
    """ Scopes thread local store """
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
        self._value: dict = {0: root_scope}  # set root scope
        self._max_scope_id: int = 0
        self._cur_scope: int = 0

    @property
    def value(self) -> dict:
        """ read-only property with dict of scopes """
        return self._value

    @property
    def current_scope(self) -> _Scope:
        return self._value[self._cur_scope]

    @current_scope.setter
    def current_scope(self, index: int) -> None:
        self._cur_scope = index

    def new_scope(self, parent: int | None):
        self._max_scope_id += 1
        new_scope = self._Scope(index=self._max_scope_id, parent=parent)
        self._value.update({self._max_scope_id: new_scope})
        self._cur_scope = self._max_scope_id


class IoC:

    scopes = Scopes()

    @staticmethod
    def resolve(key: str, *args) -> T:
        scope = IoC.scopes.current_scope
        result = None
        try:
            while not result:
                try:
                    result = scope.__getattribute__(key)(*args)
                    if not result and 'Set' in key:
                        break
                except AttributeError:
                    scope = IoC.scopes.value[scope.parent]
        except KeyError:
            raise IocResolveException(f'unresolved registration {key}')

        return result

    # @staticmethod
    # def _register(key: str, func: callable):
    #     SCOPES.current_scope.__setattr__(key, func)


# if __name__ == '__main__':
#     IoC.resolve('Scope.New', IoC.scopes, IoC.scopes.current_scope.id).execute()
#     IoC.resolve('IoC.Register', 'pow2', lambda x: x ** 2).execute()
#     print(123)


# todo: resolve circular import. IoC -> Scopes -> Register -> IoC
