import events
from commands import LogWriter
from interfaces.command import Command
from interfaces.uobject import UObject
from ioc.container import IoC


class CheckCollision(Command):
    def __init__(self, obj_a: UObject, obj_b: UObject):
        self._obj_a = obj_a
        self._obj_b = obj_b
        self.queue = IoC.resolve('Queue')

    def execute(self):
        if self._obj_a == self._obj_b:
            return

        if hasattr(self._obj_a, 'is_collised') and hasattr(self._obj_b, 'is_collised'):
            if self._obj_a.is_collised(self._obj_b):
                # HANDLE object collision
                self.queue.put(
                    LogWriter(events.CollideEvent(
                        f'Objects: {self._obj_a} {self._obj_b} are collided'))
                )
                #TODO: the logic of collision handling should be implemented here
