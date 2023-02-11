from commands.burn_fuel import BurnFuel
from commands.check_fuel import CheckFuel
from commands.macro_command import MacroCommand
from commands.move import Move
from mtypes.mixed_types import MF


class Movement(MacroCommand):
    def __init__(self, obj: MF):
        super().__init__([CheckFuel(obj), Move(obj), BurnFuel(obj)])
