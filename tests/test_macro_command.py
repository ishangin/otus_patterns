import pytest

import objects
from interfaces.command import Command
from commands.burn_fuel import BurnFuel
from commands.change_velocity import ChangeVelocity
from commands.check_fuel import CheckFuel
from commands.macro_command import MacroCommand
from commands.macro_movement import Movement
from commands.macro_rotatement import Rotatement
from commands.move import Move
from commands.rotate import Rotate
from errors.errors import CommandException
from mtypes.vector import Vector


class TestMacroCommand:

    def test_macro_command(self, mocker, mockobj):
        mocker.patch('commands.move.Move.execute')
        mocker.patch('commands.rotate.Rotate.execute')
        mocker.patch('commands.check_fuel.CheckFuel.execute')
        mocker.patch('commands.burn_fuel.BurnFuel.execute')
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        obj = objects.SpaceShip()
        MacroCommand(
            [
                Move(obj),
                Rotate(obj),
                CheckFuel(obj),
                BurnFuel(obj)
            ]
        ).execute()

        assert Move.execute.called
        assert Rotate.execute.called
        assert CheckFuel.execute.called
        assert BurnFuel.execute.called

    def test_macro_command_without_execution(self):
        """ test exception if command without execute method """

        class Cmd(Command):
            """ Wrong command stub"""
            ...

        with pytest.raises(TypeError):
            MacroCommand([Cmd()]).execute()

    # movement command test

    def test_movement(self, mocker, mockobj):
        mocker.patch('commands.check_fuel.CheckFuel.execute')
        mocker.patch('commands.move.Move.execute')
        mocker.patch('commands.burn_fuel.BurnFuel.execute')
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip()
        Movement(movable_obj).execute()
        assert CheckFuel.execute.called
        assert Move.execute.called
        assert BurnFuel.execute.called

    def test_movement_values(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(_position=Vector(10, 10), _velocity=Vector(2, -4), _fuel=10, _fuel_rate=2)
        Movement(movable_obj).execute()
        assert movable_obj.position == Vector(12, 6)
        assert movable_obj.fuel == 8

    def test_movement_error(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(_fuel=1, _fuel_rate=2)
        with pytest.raises(CommandException):
            Movement(movable_obj).execute()

    # rotatement command test

    def test_rotatement(self, mocker, mockobj):
        mocker.patch('commands.check_fuel.CheckFuel.execute')
        mocker.patch('commands.rotate.Rotate.execute')
        mocker.patch('commands.burn_fuel.BurnFuel.execute')
        mocker.patch('commands.change_velocity.ChangeVelocity.execute')
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        rotable_obj = objects.SpaceShip()
        Rotatement(rotable_obj).execute()
        assert CheckFuel.execute.called
        assert Rotate.execute.called
        assert BurnFuel.execute.called
        assert ChangeVelocity.execute.called

    def test_rotatement_values(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        movable_obj = objects.SpaceShip(
            _position=Vector(10, 10),
            _velocity=Vector(2, -4),
            _fuel=10,
            _fuel_rate=2,
            _direction=1,
            _directions_number=8,
            _angular_velocity=3
        )
        Rotatement(movable_obj).execute()
        assert movable_obj.position == Vector(10, 10)
        assert movable_obj.fuel == 8
        assert movable_obj.velocity == Vector(0, -4)

    def test_rotatement_error(self, mocker, mockobj):
        mocker.patch.object(objects, 'SpaceShip', new=mockobj)
        rotable_obj = objects.SpaceShip(_fuel=1, _fuel_rate=2)
        with pytest.raises(CommandException):
            Rotatement(rotable_obj).execute()
