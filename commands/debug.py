import os
import threading
from time import sleep

from interfaces.command import Command


class SleepCmd(Command):
    def __init__(self, sec: int):
        self._sec = sec

    def execute(self) -> None:
        sleep(self._sec)


class EmptyCmd(Command):
    def __init__(self):
        pass

    def execute(self) -> None:
        pass


class DebugCmd(Command):
    def __init__(self):
        pass

    def execute(self) -> None:
        # todo: add to print debug info
        print(threading.enumerate())
        print(os.cpu_count())
