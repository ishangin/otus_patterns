from Interfaces.command import Command
from Interfaces.rotate import Rotable


class Rotate(Command):
    def __init__(self, r: Rotable):
        self._r = r

    def execute(self):
        self._r.direction = self._r.direction + self._r.angular_velocity % self._r.directions_number
