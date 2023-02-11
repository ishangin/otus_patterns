from commands.burn_fuel import BurnFuel
from commands.change_velocity import ChangeVelocity
from commands.check_fuel import CheckFuel
from commands.macro_command import MacroCommand
from commands.rotate import Rotate
from mtypes.mixed_types import MRF


class Rotatement(MacroCommand):
    def __init__(self, obj: MRF):
        super().__init__([CheckFuel(obj), Rotate(obj), BurnFuel(obj), ChangeVelocity(obj)])
