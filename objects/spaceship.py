from interfaces.collised import Collised
from interfaces.move import Movable
from mtypes.vector import Vector
from utils import get_unique_id


class SpaceShip(Collised, Movable):
    def __init__(self, position: Vector, radius: int, velocity: Vector, owner: str):
        self._position = position
        self._radius = radius
        self._velocity = velocity
        self._id = get_unique_id()
        self._owner = owner  # token

    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, vector: Vector) -> None:
        self._position = vector

    @property
    def velocity(self) -> Vector:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Vector) -> None:
        self._velocity = value

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, value: int) -> None:
        self._radius = value

    @property
    def obj_id(self) -> int:  # todo: make interface ownable move id's into
        return self._id

    @obj_id.setter
    def obj_id(self, value: int) -> None:  # todo: make interface ownable move id's into
        self._id = value

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, value: str) -> None:
        self._owner = value
