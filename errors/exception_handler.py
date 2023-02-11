from queue import Queue

from Interfaces.command import Command
from commands.check_fuel import CheckFuel
from commands.repeater import Repeater, DoubleRepeater
from commands.log_writer import LogWriter
from commands.move import Move
from commands.rotate import Rotate


class ExceptionHandler:

    def __init__(self, queue: Queue):
        self.queue = queue
        self.ex_dispatcher = {
            Move:           self.double_repeater_handler,
            Rotate:         self.log_handler,
            CheckFuel:      self.repeater_handler,
            Repeater:       self.log_handler,
            DoubleRepeater: self.repeater_handler,
            LogWriter:      self.default_handler,
        }

    def handle(self, cmd: Command, ex: Exception):
        """
        handler selector by command or use default handler
        """
        ex_handler = self.ex_dispatcher.get(type(cmd), self.default_handler)
        ex_handler(cmd, ex)

    def default_handler(self, cmd: Command, ex: Exception):
        """
        default handler exception
        """
        print(f'{cmd=} {ex=}')

    def repeater_handler(self, cmd: Command, ex: Exception):
        """
        repeater handler exception
        """
        self.queue.put(Repeater(cmd=cmd))

    def double_repeater_handler(self, cmd: Command, ex: Exception):
        """
        double repeater handler exception
        """
        self.queue.put(DoubleRepeater(cmd=Repeater(cmd)))

    def log_handler(self, cmd: Command, ex: Exception):
        """
        Log handler exception
        """
        self.queue.put(LogWriter(ex=ex))
