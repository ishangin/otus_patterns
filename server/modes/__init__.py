from queue import Queue

from interfaces.command import Command
from interfaces.state import State


class Mode:
    def __init__(self, state: State):
        self._state = state

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        self._state = value

    def execute(self, cmd: Command):
        self._state.execute(cmd=cmd)


class Normal(State):
    def execute(self, cmd: Command) -> None:
        cmd.execute()


class MoveTo(State):
    def __init__(self, queue: Queue):
        self._queue = queue

    def execute(self, cmd: Command) -> None:
        self._queue.put(cmd)
