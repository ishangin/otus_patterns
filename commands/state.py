from queue import Queue

from interfaces.command import Command
from server.modes import Mode, MoveTo, Normal
from server.__main__ import Worker
import logging


log = logging.getLogger(__name__)


class MoveToCommand(Command):
    def __init__(self, queue: Queue, worker: Worker):
        self._queue = queue
        self._worker = worker

    def execute(self) -> None:
        log.info(f'Worker: {self._worker.id} change mode to MoveTo: {self._queue=}')
        self._worker.mode = Mode(MoveTo(self._queue))


class RunCommand(Command):
    def __init__(self, worker: Worker):
        self._worker = worker

    def execute(self) -> None:
        log.info(f'Worker: {self._worker.id} change mode to Normal')
        self._worker.mode = Mode(Normal())
