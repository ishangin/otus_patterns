from interfaces.collised import Collised
from mtypes.vector import Vector


class SpaceShip(Collised):
    def __init__(self, position: Vector, radius: int):
        self._position = position
        self._radius = radius

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def radius(self) -> int:
        return self._radius
