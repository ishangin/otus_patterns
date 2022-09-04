import logging

from interfaces.command import Command

log = logging.getLogger(__name__)


class LogWriter(Command):
    def __init__(self, ex: Exception):
        self._ex = ex

    def execute(self) -> None:
        log.exception(self._ex)
