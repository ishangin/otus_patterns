import pytest

import main
from vector import Vector
from move import Movable, Move


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


class TestMovable:

    def test_move_execute(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        movable_obj = main.SpaceShip(_position=Vector(12, 5), _velocity=Vector(-7, 3))
        Move(movable_obj).execute()
        assert movable_obj.position == Vector(5, 8)

    def test_move_without_position(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        movable_obj = main.SpaceShip(_velocity=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_move_without_velocity(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        movable_obj = main.SpaceShip(_position=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_move_without_position_setter(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj_Move)
        movable_obj = main.SpaceShip(_position=Vector(0, 0), _velocity=Vector(1, 1))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()
