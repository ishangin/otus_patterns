import logging
import threading
from queue import Empty, Queue
from typing import TypeVar

from commands.move import Move
from commands.scope import ScopeNew, ScopeSetCurrent
from errors.errors import IocResolveException
from interfaces.command import Command
from interfaces.uobject import UObject
from mtypes.vector import Vector
from objects import Space, TypeObjects
from server.message import CommandInfo
from server.message.operation import OPERATION

T = TypeVar('T')

log = logging.getLogger(__name__)


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


class InterpretCommand(Command):
    def __init__(self, queue: Queue, command_info: CommandInfo):
        self._queue = queue
        self._command_info = command_info

    def execute(self):
        try:
            game_object = IoC.resolve('GameObject', self._command_info.object_id)
        except IocResolveException:
            game_object = None

        if game_object:
            if game_object.owner != self._command_info.args.pop("jwt"):
                log.warning(f"DROP {self._command_info=} attempt to access foreign objects")
                return

        try:
            operation = OPERATION(self._command_info.operation).name.replace('_', '.')
        except ValueError as ex:
            raise ValueError(f'Wrong operation {self._command_info.operation}', ex)

        params = list(filter(None, [game_object, self._command_info.args]))
        self._queue.put(IoC.resolve(operation, *params))


class GameObjects:
    def __init__(self):
        self._store = {}

    def add_game_object(self, obj: UObject):
        self._store.update({obj.get_property("obj_id"): obj})

    def obj_exists(self, obj: UObject) -> bool:
        return obj.get_property("obj_id") in self._store.keys()

    def obj_can_access(self, obj: UObject, token: str) -> bool:
        return token == self._store[obj.get_property("obj_id")]["token"]

    def get_object(self, obj_id: int) -> UObject | None:
        return self._store.get(obj_id, {})

    @property
    def data(self) -> dict:
        return self._store


class GameCommand(Command):
    def __init__(self, arg):
        self._id = arg["game_id"]
        self._queue = arg["queue"]
        self._worker_queue = arg["worker_queue"]
        self._game_objects = GameObjects()
        self._battle_field = Space()  # use default space settings
        IoC.resolve('Scope.New', 0).execute()  # 0 args is root scope is parent for new game
        self._scope = IoC.scopes.current_scope
        IoC.resolve('IoC.Register', 'Queue', self._get_game_queue).execute()
        IoC.resolve('IoC.Register', 'GameObjects', self._get_game_objects).execute()
        IoC.resolve('IoC.Register', 'GameObject', self._get_game_object).execute()
        IoC.resolve('IoC.Register', 'BattleField', self._get_battle_field).execute()
        IoC.resolve('IoC.Register', 'Create.Object', CreateObject).execute()
        IoC.resolve('IoC.Register', 'Command.Move', Move).execute()

    def _get_game_objects(self, _):
        return self._game_objects

    def _get_game_object(self, obj_id):
        return self._game_objects.get_object(obj_id)

    def _get_battle_field(self, _):
        return self._battle_field

    def _get_game_queue(self, _):
        return self._queue

    def execute(self) -> None:
        command = None
        try:
            command = self._queue.get(timeout=1)
        except Empty:
            pass

        if command:
            log.info(f'GAME_ID: {self._id} : PID {threading.current_thread().ident} : CMD {command}')
            IoC.resolve('Scope.SetCurrent', self._scope.id).execute()
            command.execute()

        self._worker_queue.put(self)


class CreateObject(Command):
    def __init__(self, obj: dict):
        self._obj = obj

    def execute(self) -> None:
        objType = self._obj.pop("type")
        conn = self._obj.pop("conn")
        self._obj["owner"] = self._obj.pop("jwt")
        # FIXME: All object have position and velocity ???
        self._obj["position"] = Vector(*self._obj.pop("position"))
        self._obj["velocity"] = Vector(*self._obj.pop("velocity"))
        obj = TypeObjects.get(objType)(**self._obj)
        game_objects = IoC.resolve("GameObjects", -1)
        game_objects.add_game_object(obj)
        conn.send(f"OBJECT_ID: {obj.obj_id}")


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
                    if result is not None or 'Set' in key:
                        break
                except AttributeError:
                    scope = IoC.scopes.value[scope.parent]
        except KeyError:
            raise IocResolveException(f'unresolved registration {key}')

        return result
