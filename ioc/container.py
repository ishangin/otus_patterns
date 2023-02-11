import threading
from queue import Queue
from typing import TypeVar

from commands.scope import ScopeNew, ScopeSetCurrent
from interfaces.command import Command
from errors.errors import IocResolveException
from server.message import CommandInfo
from server.message.operations import OPERATIONS

__all__ = ['IoC']

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


class InterpretCommand(Command):
    def __init__(self, queue: Queue, command_info: CommandInfo):
        self._queue = queue
        self._command_info = command_info

    def execute(self):
        try:
            game_objects = IoC.resolve('GameObjects', self._command_info.object_id)
        except IocResolveException:
            game_objects = None

        try:
            operation = OPERATIONS(self._command_info.operation_id).name.replace('_', '.')
        except ValueError as ex:
            raise ValueError(f'Wrong operation {self._command_info.operation_id}', ex)

        params = [
            game_objects,
            *self._command_info.args.values()]  # FIXME: think about message format args is JSON but keys not used
        self._queue.put(
            IoC.resolve(
                operation,
                *[param for param in params if param is not None]
            )
        )


class GameCommand(Command):
    def __init__(self):
        self._queue = Queue()
        self._game_objects = {}
        IoC.resolve('Scope.New', 0).execute()  # 0 args is root scope is parent for new game
        self._scope = IoC.scopes.current_scope
        IoC.resolve('IoC.Register', 'Queue', self._get_game_queue).execute()
        IoC.resolve('IoC.Register', 'GameObjects', self._get_game_objects).execute()
        # s.games.update({len(s.games): self._queue})

    def _get_game_objects(self):
        return self._game_objects

    def _get_game_queue(self):
        return self._queue

    def execute(self) -> None:
        command = self._queue.get(timeout=1)
        if command:
            IoC.resolve('Scope.SetCurrent', self._scope.id).execute()
            command.execute()


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
        root_scope.__setattr__('Command.Interpret', InterpretCommand)
        root_scope.__setattr__('Game.New', GameCommand)

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
