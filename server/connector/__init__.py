import json
import selectors
import threading

from multiprocessing.connection import Listener
from struct import unpack

import logging

from server.message import Message, CommandInfo
# from server.message import Message, CommandInfo

HOST = '127.0.0.1'
PORT = 0
PASSWORD = 'P@$$w0rd'

log = logging.getLogger(__name__)


class Connector:

    def __init__(self, message_router: callable):
        self._selector = selectors.DefaultSelector()
        self._clients = []
        self.listener = Listener((HOST, PORT), authkey=bytes(PASSWORD, 'UTF8'))
        self._selector.register(self.listener._listener._socket.fileno(), selectors.EVENT_READ, self._accept)
        self._accept_connection_thread = threading.Thread(name='AcceptConnThread', target=self.process, daemon=True)
        self.stop_event = threading.Event()
        self.message_router = message_router

    def start(self):
        self._accept_connection_thread.start()

    def process(self):
        # log.info(f'START: AcceptConnThread (listen {HOST}:{PORT})')
        log.info(f'START: AcceptConnThread (listen {self.listener._listener._socket.getsockname()})')

        while not self.stop_event.is_set():
            events = self._selector.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        log.info('STOP: AcceptConnThread')

    def stop(self):
        for client in self._clients:
            client['connection'].close()
        self.stop_event.set()
        self._accept_connection_thread.join()
        self.listener.close()

    def _accept(self, socket, mask):
        connection = self.listener.accept()
        self._clients.append({'connection': connection, 'address': self.listener.last_accepted})
        log.info(f'Client connected {self.listener.last_accepted}')
        self._selector.register(connection, selectors.EVENT_READ, self._on_message_received)

    def _on_message_received(self, connection, mask):
        recv = connection.recv()
        # 3x int  game_id, object_id, operation_id
        (game_id, object_id, operation_id), args = unpack('3I', recv[:12]), recv[12:]
        try:
            args = json.loads(args.decode('utf-8'))
        except Exception as ex:
            log.exception(f'receive wrong format message {recv=} {ex=}')
            return
        message = Message(
            game_id=game_id,
            command_info=CommandInfo(
                object_id=object_id,
                operation_id=operation_id,
                args=args
            )
        )
        self.message_router(message)
