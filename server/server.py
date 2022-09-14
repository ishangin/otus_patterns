from enum import Enum
from queue import Queue, Empty
from random import choice
import threading
import logging

# from commands.game import GameCommand
import commands
from db import GAMES
# from commands.worker import NewWorker, StopWorker, SoftStopWorker
from errors.exception_handler import ExceptionHandler
from interfaces.command import Command
from ioc.container import IoC
from server.connector import Connector

from server.message import Message
from server.message.operations import OPERATIONS

__all__ = ['Server']

log = logging.getLogger(__name__)


class STATUS (Enum):
    STOPPED = 0
    RUNNING = 1


class Worker:
    def __init__(self, worker_id: int, queue: Queue, ex_handler: ExceptionHandler):
        self.id = worker_id
        self.status = STATUS.STOPPED
        self._worker_thread = threading.Thread(name=f'worker{self.id}', target=self._process)
        self._start_event = threading.Event()
        self._stop_event = threading.Event()
        self._soft_stop_event = threading.Event()
        self.queue = queue
        self._ex_handler = ex_handler

    def stop(self):
        self._stop_event.set()
        try:    # don't like for me. think about fix it
            self._worker_thread.join()
        except RuntimeError:  # if _thread == current_thread
            pass
        self.status = STATUS.STOPPED

    def soft_stop(self):
        self._soft_stop_event.set()
        try:    # don't like for me. think about fix it.
            self._worker_thread.join()
        except RuntimeError:  # if _thread == current_thread
            pass
        self.status = STATUS.STOPPED

    def start(self):
        self._worker_thread.start()
        self._start_event.wait()
        self.status = STATUS.RUNNING

    def _process(self) -> None:
        self._start_event.set()
        log.info(f'START: {self._worker_thread.name} : ID {self.id} : THREAD PID {threading.current_thread().ident}')

        while True:
            if self._stop_event.is_set():
                break
            try:
                cmd = self.queue.get(block=True, timeout=1)
            except Empty:
                if self._soft_stop_event.is_set():
                    log.info(f'THREAD SOFT STOP {self._worker_thread.name} : ID {self.id} : PID {threading.current_thread().ident}')
                    return
                else:
                    continue
            log.info(f'{self._worker_thread.name} : ID {self.id} : PID {threading.current_thread().ident} : CMD {cmd}')
            try:
                cmd.execute()

            except Exception as ex:
                self._ex_handler.handle(cmd, ex)
        log.info(f'STOP: {self._worker_thread.name} : ID {self.id} : THREAD PID {threading.current_thread().ident}')


class Server:

    def __init__(self):
        self._connector = Connector(message_router=self.message_router)
        self._workers = dict()
        self.games = dict()

    def spawn_worker(self):
        _q = Queue()
        worker = Worker(
            len(self._workers),
            queue=_q,
            ex_handler=ExceptionHandler(queue=_q)
        )
        self._workers.update({len(self._workers): worker})
        worker.start()

    def stop_worker(self, worker_id: int, force: bool = False):
        if force:
            self._workers.get(worker_id).stop()
        else:
            self._workers.get(worker_id).soft_stop()
        self._workers.pop(worker_id)

    def start(self):
        self._connector.start()
        self.spawn_worker()

    def stop(self):
        self._connector.stop()
        for _, worker in self._workers.items():
            worker.stop()
        self._workers.clear()

    def put_command(self, cmd: Command, game_id: int = None):
        if game_id is not None:
            worker = self.games.get(game_id, None)
            worker.queue.put(cmd)
        else:
            log.warning(f'DROP {cmd=}, game_id is None')

    def message_router(self, messsage: Message):
        if messsage.command_info.operation_id == OPERATIONS.Game_New.value:
            worker = self.get_worker()  # get free (now random) worker
            game_id = self.new_game(worker)
        else:
            game_id = messsage.game_id
            jwt = messsage.command_info.args.get('jwt')
            if not jwt or jwt not in GAMES[game_id]['tokens']:
                log.warning(f'DROP {messsage=}, invalid token')
                return
            worker = self.games.get(messsage.game_id)
        if worker:
            self.put_command(cmd=IoC.resolve('Command.Interpret', worker.queue, messsage.command_info),
                             game_id=game_id)
        else:
            log.warning(f'DROP {messsage=}, worker not found for {game_id=}')

    def new_game(self, worker: Worker) -> int:
        """
        return new Game_ID
        """
        game_id = len(self.games)
        self.games.update({game_id: worker})  # game <-> worker matching
        return game_id

    def stop_game(self, game_id: int) -> None:
        """
        stop game by game_id
        """
        self.games.pop(game_id)

    def get_worker(self) -> Worker:
        return choice(self._workers)


IoC.resolve('IoC.Register', 'Worker.New', commands.NewWorker).execute()
IoC.resolve('IoC.Register', 'Worker.Stop',commands.StopWorker).execute()
IoC.resolve('IoC.Register', 'Worker.SoftStop', commands.SoftStopWorker).execute()
# IoC.resolve('IoC.Register', 'Game.New', GameCommand).execute()


if __name__ == '__main__':
    s = Server()
    s.start()
    # s.put_command(LogWriter(ValueError('test')))
    IoC.resolve('Worker.New', s).execute()
    # IoC.resolve('Game.New').execute()
    s.put_command(IoC.resolve('Game.New'))
    s.stop()
    print('END')
