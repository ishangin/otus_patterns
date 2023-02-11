import pytest

from vector import Vector
from move import Movable
from rotate import Rotable
from fuel import Fuelable


class MockObj(Movable, Rotable, Fuelable):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

# Movable

    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, vector: Vector) -> None:
        self._position = vector

    @property
    def velocity(self) -> Vector:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Vector) -> None:
        self._velocity = value

# Rotable

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, direction: int) -> None:
        self._direction = direction

    @property
    def directions_number(self) -> int:
        return self._directions_number

    @property
    def angular_velocity(self) -> int:
        return self._angular_velocity

# Fuel

    @property
    def fuel(self) -> int:
        return self._fuel

    @fuel.setter
    def fuel(self, value: int) -> None:
        self._fuel = value

    @property
    def fuel_rate(self) -> int:
        return self._fuel_rate


@pytest.fixture()
def mockobj():
    return MockObj
