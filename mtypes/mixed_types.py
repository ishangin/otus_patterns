from typing import TypeVar

from interfaces.move import Movable
from interfaces.rotate import Rotable
from interfaces.fuel import Fuelable

__all__ = ['MR', 'MF', 'RF', 'MRF']

# M - Movable, R - Rotable, F - Fielable
MR = TypeVar('MR', Movable, Rotable)
MF = TypeVar('MF', Movable, Fuelable)
RF = TypeVar('RF', Rotable, Fuelable)
MRF = TypeVar('MRF', Movable, Rotable, Fuelable)
