from Interfaces.command import Command
from main import log


class LogWriter(Command):
    def __init__(self, ex: Exception):
        self._ex = ex

    def execute(self) -> None:
        log.exception(self._ex)
