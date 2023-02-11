from Interfaces.command import Command


class Repeater(Command):
    def __init__(self, cmd: Command):
        self._cmd = cmd

    def execute(self) -> None:
        self._cmd.execute()
