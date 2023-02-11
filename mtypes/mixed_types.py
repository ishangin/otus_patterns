from typing import TypeVar

from Interfaces.move import Movable
from Interfaces.rotate import Rotable
from Interfaces.fuel import Fuelable

__all__ = ['MR', 'MF', 'RF', 'MRF']

# M - Movable, R - Rotable, F - Fielable
MR = TypeVar('MR', Movable, Rotable)
MF = TypeVar('MF', Movable, Fuelable)
RF = TypeVar('RF', Rotable, Fuelable)
MRF = TypeVar('MRF', Movable, Rotable, Fuelable)
