from abc import ABC, abstractmethod

from command import Command
from vector import Vector

__all__ = ['Movable', 'Move']


class Movable(ABC):
    """ Movable interface"""

    @property
    @abstractmethod
    def position(self) -> Vector:
        """
        get position
        :return: Vector
        """
        ...

    @position.setter
    @abstractmethod
    def position(self, v: Vector) -> Vector:
        """
        set position
        :return: Vector
        """
        ...

    @property
    @abstractmethod
    def velocity(self) -> Vector:
        """
        get velocity
        :return: Vector velocity
        """
        ...

    @velocity.setter
    def velocity(self, value: Vector) -> None:
        """
        setter velocity
        :value: Vector
        :return: None
        """
        ...


# class MovableObject(Movable):
#     def __init__(self, o: UObject):
#         self._o = o
#
#     def get_position(self) -> Vector:
#         return self._o.get_property('position')
#
#     def set_position(self, vector: Vector) -> None:
#         self._o.set_property('position', vector)
#
#     def get_velocity(self) -> Vector:
#         d = self._o.get_property('direction')
#         n = self._o.get_property('directions_number')
#         v = self._o.get_property('velocity')
#         return Vector(x=v.x * cos(d / 360 * n),
#                       y=v.y * sin(d / 360 * n))


class Move(Command):
    def __init__(self, m: Movable):
        self._m = m

    def execute(self) -> None:
        self._m.position = self._m.position.add(self._m.velocity)
