from interfaces.command import Command
from ioc.container import IoC
from objects import TypeObjects


class CreateObject(Command):
    def __init__(self, obj: dict):
        self._obj = obj

    def execute(self) -> None:
        obj = TypeObjects.get(self._obj.pop("type"))(**self._obj)
        gameobjects = IoC.resolve('GameObjects')
        gameobjects.append(obj)
        self._obj["conn"].send(f"OBJECT_ID: {obj.obj_id}")
