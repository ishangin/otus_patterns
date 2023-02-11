from dataclasses import dataclass
from abc import ABC, abstractmethod
from math import sin, cos
from typing import Any

__all__ = [
    'SpaceShip',
    'Vector',
    'Movable',
    'Move',
    'Rotable',
    'Rotate'
]


@dataclass
class Vector:
    """
    type Vector(x, y)
    """
    x: float
    y: float

    def add(self, vec: "Vector") -> "Vector":
        return Vector(self.x + vec.x, self.y + vec.y)


# class UObject(ABC):
#
#     @abstractmethod
#     def get_property(self, name: str) -> Any:
#         raise NotImplementedError
#
#     @abstractmethod
#     def set_property(self, name: str, value: Any) -> None:
#         raise NotImplementedError


class Movable(ABC):
    """ Movable interface"""

    @abstractmethod
    def get_position(self) -> Vector:
        """
        get position
        :return: Vector
        """
        raise NotImplementedError

    @abstractmethod
    def set_position(self, vector: Vector) -> None:
        """
        set position
        :param vector: new position
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_velocity(self) -> Vector:
        """
        get velocity
        :return: Vector velocity
        """
        raise NotImplementedError


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


class Move:
    def __init__(self, m: Movable):
        self._m = m

    def execute(self):
        self._m.set_position(self._m.get_position().add(self._m.get_velocity()))


class Rotable(ABC):
    @abstractmethod
    def get_direction(self) -> int:
        """

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def set_direction(self, direction: int) -> None:
        """

        :param direction:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_directions_number(self) -> int:
        """

        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_angular_velocity(self) -> int:
        """

        :return:
        """
        raise NotImplementedError


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


class Rotate:
    def __init__(self, r: Rotable):
        self._r = r

    def execute(self):
        self._r.set_direction(
            self._r.get_direction() + self._r.get_angular_velocity() % self._r.get_directions_number()
        )


class SpaceShip(Movable, Rotable):
    __slots__ = ('_position', '_velocity', '_direction', '_directions_number')

    def __init__(self, *args, **kwargs):
        pass

# class SpaceShip(UObject):
#
#     def get_property(self, name: str) -> Any:
#         return self.__getattribute__(name)
#
#     def set_property(self, name: str, value: Any) -> None:
#         self.__setattr__(name, value)
#
#
# s = SpaceShip()
# s.set_property('position', Vector(12, 5))
# s.set_property('velocity', Vector(-7, 3))
# s.set_property('direction', 0)
# s.set_property('directions_number', 8)
# sm = MovableObject(s)
#
# Move(sm).execute()
