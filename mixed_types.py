from typing import TypeVar

from move import Movable
from rotate import Rotable
from fuel import Fuelable

__all__ = ['MR', 'MF', 'RF', 'MRF']

# M - Movable, R - Rotable, F - Fielable
MR = TypeVar('MR', Movable, Rotable)
MF = TypeVar('MF', Movable, Fuelable)
RF = TypeVar('RF', Rotable, Fuelable)
MRF = TypeVar('MRF', Movable, Rotable, Fuelable)
