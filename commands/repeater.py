from Interfaces.command import Command


class _BaseRepeater(Command):
    def __init__(self, cmd: Command):
        self._cmd = cmd

    def execute(self) -> None:
        self._cmd.execute()


class Repeater(_BaseRepeater):
    ...


class DoubleRepeater(_BaseRepeater):
    ...
