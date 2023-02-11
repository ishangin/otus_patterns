from typing import Any

import pytest


from interfaces.move import Movable
from interfaces.rotate import Rotable
from interfaces.fuel import Fuelable
from interfaces.uobject import UObject
from mtypes.vector import Vector


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


class MockObj_Move(Movable):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def velocity(self) -> Vector:
        return self._velocity


class MockObj_Rotate(Rotable):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def directions_number(self) -> int:
        return self._direction_number

    @property
    def angular_velocity(self) -> int:
        return self._angular_velocity


class MockObj_Fuel(Fuelable):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def fuel(self) -> int:
        return self._fuel

    @fuel.setter
    def fuel(self, value: int) -> None:
        self._fuel = value

    @property
    def fuel_rate(self) -> int:
        return self._fuel_rate


class ScopesTest:

    def new_scope(self):
        ...

    def current_scope(self):
        ...


class UObj(UObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def get_property(self, name: str) -> Any:
        return self.__getattribute__(name)

    def set_property(self, name: str, value: Any) -> None:
        self.__setattr__(name, value)


@pytest.fixture()
def mockobj():
    return MockObj


@pytest.fixture()
def mockobj_move():
    return MockObj_Move


@pytest.fixture()
def mockobj_rotate():
    return MockObj_Rotate


@pytest.fixture()
def mockobj_fuel():
    return MockObj_Fuel


@pytest.fixture()
def scopes_test():
    return ScopesTest


@pytest.fixture()
def uobj():
    return UObj
