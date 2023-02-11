from abc import ABC, abstractmethod

from math import sin, cos, pi

from command import Command
from move import Movable
from vector import Vector

__all__ = ['Rotable', 'Rotate']


class Rotable(ABC):
    """ Rotable interface """

    @property
    @abstractmethod
    def direction(self) -> int:
        """

        :return:
        """
        ...

    @direction.setter
    @abstractmethod
    def direction(self, direction: int) -> None:
        """

        :param direction:
        :return:
        """
        ...

    @property
    @abstractmethod
    def directions_number(self) -> int:
        """

        :return:
        """
        ...

    @property
    @abstractmethod
    def angular_velocity(self) -> int:
        """

        :return:
        """
        ...


# class RotableObject(Rotable):
#     def __init__(self, o: UObject):
#         self._o = o
#
#     def get_direction(self) -> int:
#         return self._o.get_property('direction')
#
#     def set_direction(self, direction: int) -> None:
#         self._o.set_property('direction', direction)
#
#     def get_direction_number(self) -> int:
#         return self._o.get_property('directions_number')
#
#     def get_angular_velocity(self) -> int:
#         return self._o.get_property('angular_velocity')


class Rotate(Command):
    def __init__(self, r: Rotable):
        self._r = r

    def execute(self):
        self._r.direction = self._r.direction + self._r.angular_velocity % self._r.directions_number


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
            self._m.velocity = Vector(x=round(v.x + v.x * cos((2 * pi * d) / n), 5),
                                      y=round(v.y + v.y * sin((2 * pi * d) / n), 5))
