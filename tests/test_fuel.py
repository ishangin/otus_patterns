import pytest

import main
from Interfaces.fuel import Fuelable
from commands.burn_fuel import BurnFuel
from commands.check_fuel import CheckFuel
from errors.errors import CommandException


class MockObj_Fuel(Fuelable):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def fuel(self) -> int:
        return self._fuel

    @property
    def fuel_rate(self) -> int:
        return self._fuel_rate


class TestFuelable:

    # CheckFuel

    def test_check_fuel(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel=10, _fuel_rate=3)
        assert CheckFuel(fuelable_obj).execute() is None

    def test_check_fuel_exc(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel=2, _fuel_rate=3)
        with pytest.raises(CommandException) as ex:
            CheckFuel(fuelable_obj).execute()
        assert str(ex.value) == "low fuel"

    def test_check_fuel_without_fuel(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel_rate=3)
        with pytest.raises(AttributeError):
            CheckFuel(fuelable_obj).execute()

    def test_check_fuel_without_fuel_rate(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel=10)
        with pytest.raises(AttributeError):
            CheckFuel(fuelable_obj).execute()

    # BurnFuel

    def test_burn_fuel(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel=10, _fuel_rate=3)
        BurnFuel(fuelable_obj).execute()
        assert fuelable_obj.fuel == 7

    def test_burn_fuel_without_fuel(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel_rate=3)
        with pytest.raises(AttributeError):
            BurnFuel(fuelable_obj).execute()

    def test_burn_fuel_without_fuel_rate(self, mocker, mockobj):
        mocker.patch.object(main, 'SpaceShip', new=mockobj)
        fuelable_obj = main.SpaceShip(_fuel=10)
        with pytest.raises(AttributeError):
            BurnFuel(fuelable_obj).execute()

    def test_burn_fuel_without_fuel_setter(self, mocker):
        mocker.patch.object(main, 'SpaceShip', new=MockObj_Fuel)
        fuelable_obj = main.SpaceShip(_fuel=2, _fuel_rate=3)
        with pytest.raises(AttributeError):
            BurnFuel(fuelable_obj).execute()
