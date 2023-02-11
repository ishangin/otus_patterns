import pytest

from adapters import AdapterMetaclass
from commands.move import Move
from commands.rotate import Rotate
from interfaces.move import Movable
from interfaces.rotate import Rotable
from ioc.container import IoC
from mtypes.vector import Vector


class TestAdapters:
    """ tests to adapters generator """

    def test_adapter_creator0(self, uobj):
        """ create adapter with IoC """
        IoC.resolve('Scope.New', IoC.scopes.current_scope.id).execute()
        IoC.resolve('IoC.Register', 'Movable.Position.Get', lambda o: o.get_property('position')).execute()
        IoC.resolve('IoC.Register', 'Movable.Position.Set', lambda o, val: o.set_property('position', val)).execute()
        IoC.resolve('IoC.Register', 'Movable.Velocity.Get', lambda o: o.get_property('velocity')).execute()
        IoC.resolve('IoC.Register', 'Movable.Velocity.Set', lambda o, val: o.set_property('velocity', val)).execute()
        IoC.resolve('IoC.Register', 'Command.Move', lambda o: Move(o)).execute()
        obj = uobj(position=Vector(2, 3), velocity=Vector(4, -1))
        move_adapter = IoC.resolve('Adapter.Create', Movable, obj)
        # Assert get properties
        assert move_adapter.position == Vector(2, 3)
        assert move_adapter.velocity == Vector(4, -1)
        # Assert direct setting  properties
        move_adapter.position = Vector(5, 6)
        move_adapter.velocity = Vector(1, -2)
        assert move_adapter.position == Vector(5, 6)
        assert move_adapter.velocity == Vector(1, -2)
        # Assert after Move command
        IoC.resolve('Command.Move', obj).execute()
        assert move_adapter.position == Vector(6, 4)
        assert move_adapter.velocity == Vector(1, -2)

    def test_adapter_creator1(self, uobj):
        """ create adapter without IoC """
        class RotableAdapter(metaclass=AdapterMetaclass):
            interface = Rotable
        IoC.resolve('Scope.New', IoC.scopes.current_scope.id).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Direction.Get',
            lambda o: o.get_property('direction')
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Direction.Set',
            lambda o, val: o.set_property('direction', val)
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Directions_number.Get',
            lambda o: o.get_property('directions_number')
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Directions_number.Set',
            lambda o, val: o.set_property('directions_number', val)
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Angular_velocity.Get',
            lambda o: o.get_property('angular_velocity')
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Rotable.Angular_velocity.Set',
            lambda o, val: o.set_property('angular_velocity', val)
        ).execute()
        IoC.resolve(
            'IoC.Register',
            'Command.Rotate',
            lambda o: Rotate(o)
        ).execute()
        obj = uobj(direction=2,
                   directions_number=8,
                   angular_velocity=1)
        rotate_adapter = RotableAdapter(obj)
        assert rotate_adapter.direction == 2
        assert rotate_adapter.directions_number == 8
        assert rotate_adapter.angular_velocity == 1
        rotate_adapter.direction = 3
        assert rotate_adapter.direction == 3
        with pytest.raises(AttributeError):  # directions_number and angular_velocity is read only props
            rotate_adapter.directions_number = 4
        with pytest.raises(AttributeError):
            rotate_adapter.angular_velocity = 2
        IoC.resolve('Command.Rotate', obj).execute()
        assert rotate_adapter.direction == 4
        assert rotate_adapter.directions_number == 8
        assert rotate_adapter.angular_velocity == 1
