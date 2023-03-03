import pytest

import objects
from commands.move import Move
from mtypes.vector import Vector


class TestMovable:

    def test_move_execute(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(_position=Vector(12, 5), _velocity=Vector(-7, 3))
        Move(movable_obj).execute()
        assert movable_obj.position == Vector(5, 8)

    def test_move_without_position(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(_velocity=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_move_without_velocity(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(_position=Vector(0, 0))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()

    def test_move_without_position_setter(self, mocker, mockobj_move):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj_move)
        movable_obj = objects.SpaceShip(_position=Vector(0, 0), _velocity=Vector(1, 1))
        with pytest.raises(AttributeError):
            Move(movable_obj).execute()
