from queue import Queue

from interfaces.command import Command
from interfaces.move import Movable
from errors.exception_handler import ExceptionHandler
from mtypes.vector import Vector


class MoveObj(Movable):
    def __init__(self, position: Vector, velocity: Vector):
        self._position = position
        self._velocity = velocity

    @property
    def position(self) -> Vector:
        return self._position

    # @position.setter
    # def position(self, position: Vector) -> None:
    #     self._position = position

    @property
    def velocity(self) -> Vector:
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: Vector) -> None:
        self._velocity = velocity


o = MoveObj(position=Vector(1, 2), velocity=Vector(0, 0))


class Server:
    def __init__(self):
        self._queue = Queue()
        self.ex_handler = ExceptionHandler(self._queue)

    def start(self):
        while True:
            cmd = self._queue.get()
            try:
                cmd.execute()
            except Exception as ex:
                self.ex_handler.handle(cmd, ex)

    def put_command(self, cmd: Command):
        self._queue.put(cmd)


# s = Server()
# s.put_command(Move(o))
# s.start()
