import logging
from server.server import Server
# import sys
# from typing import Any
#
# import objects
#
# from interfaces.uobject import UObject


FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


# class SpaceShip(Movable, Rotable, Fuelable):
#     __slots__ = ('position', 'velocity', 'direction', 'directions_number', 'angular_velocity')
#
#     def __init__(self, *args, **kwargs):
#         pass
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
    s = Server()
    s.start()
    # s.put_command(LogWriter(ValueError('test')))
    # IoC.resolve('Worker.New', s).execute()
    # IoC.resolve('Game.New').execute()
    # s.put_command(IoC.resolve('Game.New'))
    s.stop()
    print('END')

    # server_start_cmd = [sys.executable, '-m', 'server']
    # subprocess.Popen('')
