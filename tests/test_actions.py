import pytest

import main
from main import *


class MockObj(Movable, Rotable):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

# Movable
    def get_position(self) -> Vector:
        return self._position

    def set_position(self, vector: Vector) -> None:
        self._position = vector

    def get_velocity(self) -> Vector:
        return self._velocity

# Rotable
    def get_direction(self) -> int:
        return self._direction

    def set_direction(self, direction: int) -> None:
        self._direction = direction

    def get_directions_number(self) -> int:
        return self._directions_number

    def get_angular_velocity(self) -> int:
        return self._angular_velocity


class TestMovable:

    def test_move_execute(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        movable_obj = main.SpaceShip(_position=Vector(12, 5), _velocity=Vector(-7, 3))
        Move(movable_obj).execute()
        assert movable_obj.get_position() == Vector(5, 8)

    def test_without_position(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        movable_obj = main.SpaceShip(_velocity=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_without_velocity(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        movable_obj = main.SpaceShip(_position=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_without_set_position(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        mocker.patch.object(main.SpaceShip, 'set_position', side_effect=AttributeError('set_position not found'))
        movable_obj = main.SpaceShip(_position=Vector(0, 0), _velocity=Vector(1, 1))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()


class TestRotable:

    def test_rotate_execute(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8, _angular_velocity=2)
        Rotate(rotable_obj).execute()
        assert rotable_obj.get_direction() == 5

    def test_without_direction(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        rotable_obj = main.SpaceShip(_directions_number=8, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_without_directions_number(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        rotable_obj = main.SpaceShip(_direction=3, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_without_directions_angular_velocity(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_without_set_direction(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj)
        mocker.patch.object(main.SpaceShip, 'set_direction', side_effect=AttributeError('set_direction not found'))
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Move(rotable_obj).execute()
