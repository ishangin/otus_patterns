from Interfaces.command import Command
from commands.repeater import Repeater


class DoubleRepeater(Command):
    def __init__(self, cmd: Repeater):
        self._cmd = cmd

    def execute(self) -> None:
        self._cmd.execute()
