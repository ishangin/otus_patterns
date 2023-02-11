import logging
# import subprocess
# import sys

from Interfaces.fuel import Fuelable
from Interfaces.move import Movable
from Interfaces.rotate import Rotable


__all__ = ['SpaceShip', 'log']

# from mtypes.vector import Vector

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
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


if __name__ == '__main__':
    pass

    # server_start_cmd = [sys.executable, '-m', 'server']
    # subprocess.Popen('')
