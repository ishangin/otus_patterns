import logging

from fuel import Fuelable
from move import Movable
from rotate import Rotable


__all__ = ['SpaceShip', 'log']

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)

# class UObject(ABC):
#
#     @abstractmethod
#     def get_property(self, name: str) -> Any:
#         raise NotImplementedError
#
#     @abstractmethod
#     def set_property(self, name: str, value: Any) -> None:
#         raise NotImplementedError


class SpaceShip(Movable, Rotable, Fuelable):
    __slots__ = ('position', 'velocity', 'direction', 'directions_number', 'angular_velocity')

    def __init__(self, *args, **kwargs):
        pass

# class SpaceShip(UObject):
#
#     def get_property(self, name: str) -> Any:
#         return self.__getattribute__(name)
#
#     def set_property(self, name: str, value: Any) -> None:
#         self.__setattr__(name, value)
#
#
# s = SpaceShip()
# s.set_property('position', Vector(12, 5))
# s.set_property('velocity', Vector(-7, 3))
# s.set_property('direction', 0)
# s.set_property('directions_number', 8)
# sm = MovableObject(s)
#
# Move(sm).execute()
