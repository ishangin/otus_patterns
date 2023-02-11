from math import cos, sin, pi

from interfaces.command import Command
from interfaces.move import Movable
from interfaces.rotate import Rotable
from mtypes.vector import Vector


class ChangeVelocity(Command):
    """
    Command to change velocity vector when moving object rotate
    """
    def __init__(self, m: Movable | Rotable):
        self._m = m

    def execute(self) -> None:
        if self._m.velocity != Vector(0, 0):  # if object is moving
            d = self._m.direction
            n = self._m.directions_number
            v = self._m.velocity

            # rounded 1e-5
            self._m.velocity = Vector(x=int(v.x + v.x * cos((2 * pi * d) / n)),
                                      y=int(v.y + v.y * sin((2 * pi * d) / n)))
