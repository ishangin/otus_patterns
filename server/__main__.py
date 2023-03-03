import json
import struct
from enum import Enum
from queue import Queue, Empty
from random import choice
import threading
import logging
from time import sleep

# from commands.game import GameCommand
import commands
from db import GAMES
# from commands.worker import NewWorker, StopWorker, SoftStopWorker
from errors.exception_handler import ExceptionHandler
from interfaces.command import Command
from interfaces.state import State
from ioc.container import IoC
from server.connector import Connector, AuthServiceConnector

from mtypes.net import Address
from server.message import Message
from server.message.operation import OPERATION

from server.modes import Mode, Normal

__all__ = ['Server', 'Worker']

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


class STATUS (Enum):
    STOPPED = 0
    RUNNING = 1


class Worker:
    def __init__(self, worker_id: int, queue: Queue, ex_handler: ExceptionHandler, mode: State = Normal()):
        self.id = worker_id
        self.status = STATUS.STOPPED
        self._worker_thread = threading.Thread(name=f'worker{self.id}', target=self._process)
        self._start_event = threading.Event()
        self._stop_event = threading.Event()
        self._soft_stop_event = threading.Event()
        self.queue = queue
        self._ex_handler = ex_handler
        self.mode = Mode(mode)

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
                    thread = {'name': self._worker_thread.name,
                              'id': threading.current_thread().ident}
                    log.info(f'THREAD SOFT STOP {thread["name"]} : ID {self.id} : PID {thread["id"]}')
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

    def __init__(self, auth_service_addr: Address):
        self._connector = Connector(message_router=self.message_router)
        self._auth_connector = AuthServiceConnector(auth_service_addr, message_router=self.message_router)
        self._workers = dict()
        self.games = GAMES

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
        self._auth_connector.start()
        self.spawn_worker()

    def stop(self):
        self._connector.stop()
        for _, worker in self._workers.items():
            worker.stop()
        self._workers.clear()

    def put_command(self, cmd: Command, game_id: int = None):
        if game_id is not None:
            worker = self.games[game_id]["worker"]
            worker.queue.put(cmd)
        else:
            log.warning(f'DROP {cmd=}, game_id is None')

    def message_router(self, message: Message):
        match message.command_info.operation:
            case OPERATION.Get_Token:
                # todo: move to Message.conn and AuthService support that
                message.command_info.args.update({"id": message.conn})
                self._auth_connector.send(
                    struct.pack(
                        "I",
                        message.command_info.operation.value) + bytes(json.dumps(message.command_info.args), "UTF8"))
                return
            case OPERATION.Auth_Response:
                # todo: message.command_info.args["id"] -> message.conn
                self._connector.clients[message.command_info.args["id"]]["connection"].send(
                    "TOKEN: " + message.command_info.args["jwt"])

                # add user token to his games after success auth
                if len(message.command_info.args["jwt"]) > 100:  # todo: temporary hack. need check auth status
                    user_games_id = [_id
                                     for _id, games in self.games.items()
                                     if int(message.command_info.args["user_id"]) in games["players"]]
                    [self.games[game_id]["tokens"].append(message.command_info.args["jwt"])
                     for game_id in user_games_id]
                return
            case OPERATION.Game_New:
                worker = self.get_worker()  # get free (now random) worker
                game_id = self.new_game(worker)
                # add first token. other tokens added when users auth completed
                self.games[game_id]["tokens"].append(message.command_info.args["jwt"])
                self.games[game_id]["players"] = message.command_info.args["players"]  # MIND: this mast be in IoC!!!
                message.command_info.args.pop("jwt")
                message.command_info.args.pop("players")
                message.command_info.args["game_id"] = game_id
                message.command_info.args["queue"] = self.games[game_id]["queue"]
                message.command_info.args["worker_queue"] = worker.queue  # GameCommand place in worker queue myself
                q = worker.queue
                self._connector.clients[message.conn]["connection"].send("GAME_ID: " + str(game_id))
            case _:
                game_id = message.game_id
                jwt = message.command_info.args["jwt"]
                if jwt not in GAMES[game_id]["tokens"]:
                    log.warning(f"DROP {message=}, invalid token")
                    return
                worker = self.games.get(message.game_id)
                q = self.games[game_id]["queue"]
                if message.command_info.operation == OPERATION.Create_Object:
                    message.command_info.args.update({"conn": self._connector.clients[message.conn]["connection"]})

        if worker:
            self.put_command(cmd=IoC.resolve('Command.Interpret', q, message.command_info),
                             game_id=game_id)
        else:
            log.warning(f'DROP {message=}, worker not found for {game_id=}')

    def new_game(self, worker: Worker) -> int:
        """
        return new Game_ID
        """
        game_id = len(self.games)
        # game <-> worker matching
        self.games.update({game_id: {"worker": worker, "tokens": [], "players": [], "queue": Queue()}})
        return game_id

    def stop_game(self, game_id: int) -> None:
        """
        stop game by game_id
        """
        self.games.pop(game_id)

    def get_worker(self) -> Worker:
        return choice(self._workers)

    def change_worker_mode(self, worker_id: int, mode: State):
        self._workers[worker_id].mode = Mode(mode)


IoC.resolve('IoC.Register', 'Worker.New', commands.NewWorker).execute()
IoC.resolve('IoC.Register', 'Worker.Stop', commands.StopWorker).execute()
IoC.resolve('IoC.Register', 'Worker.SoftStop', commands.SoftStopWorker).execute()
# IoC.resolve('IoC.Register', 'Game.New', GameCommand).execute()


if __name__ == '__main__':
    s = Server(auth_service_addr=("127.0.0.1", 5578, bytes("P@$$w0rd", "UTF8")))
    s.start()
    while True:
        sleep(5)
        # todo: create valid stop signal to server

    s.stop()
