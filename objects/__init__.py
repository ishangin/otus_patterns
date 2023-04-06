from .bullet import Bullet
from .space import Space
from .spaceship import SpaceShip
from .region import Region


TypeObjects = {
    "Bullet": Bullet,
    "Space": Space,
    "SpaceShip": SpaceShip,
    "Region": Region,
}

__all__ = [Bullet, Space, SpaceShip, Region, TypeObjects]
