import pytest

import main
from commands.change_velocity import ChangeVelocity
from commands.rotate import Rotate
from mtypes.vector import Vector


class TestRotable:

    # rotate

    def test_rotate_execute(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8, _angular_velocity=2)
        Rotate(rotable_obj).execute()
        assert rotable_obj.direction == 5

    def test_rotate_without_direction(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        rotable_obj = main.SpaceShip(_directions_number=8, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_rotate_without_directions_number(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        rotable_obj = main.SpaceShip(_direction=3, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_rotate_without_angular_velocity(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    def test_rotate_without_direction_setter(self, mocker, mockobj_rotate):
        mocker.patch.object(main, 'SpaceShip', new=mockobj_rotate)
        rotable_obj = main.SpaceShip(_direction=3, _directions_number=8, _angular_velocity=2)
        with pytest.raises(AttributeError):
            Rotate(rotable_obj).execute()

    # change velocity

    def test_change_velocity(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        obj = main.SpaceShip(_velocity=Vector(2, -4), _direction=4, _directions_number=8)
        ChangeVelocity(obj).execute()
        assert obj.velocity == Vector(0, -4)

    def test_change_velocity_without_velocity(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        obj = main.SpaceShip(_direction=4, _directions_number=8)
        with pytest.raises(AttributeError):
            ChangeVelocity(obj).execute()

    def test_change_velocity_without_direction(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        obj = main.SpaceShip(_velocity=Vector(2, -4), _directions_number=8)
        with pytest.raises(AttributeError):
            ChangeVelocity(obj).execute()

    def test_change_velocity_without_directions_number(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        obj = main.SpaceShip(_velocity=Vector(2, -4), _direction=4)
        with pytest.raises(AttributeError):
            ChangeVelocity(obj).execute()

    def test_change_velocity_without_velocity_setter(self, mocker, mockobj_rotate):
        mocker.patch.object(main, 'SpaceShip', new=mockobj_rotate)
        rotable_obj = main.SpaceShip(_velocity=Vector(2, -4), _direction=4, _directions_number=8)
        with pytest.raises(AttributeError):
            ChangeVelocity(rotable_obj).execute()
