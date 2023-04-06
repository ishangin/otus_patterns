import json
import logging
import selectors
import threading
from multiprocessing.connection import Client, Connection, Listener
from struct import unpack
from uuid import uuid4

from mtypes.net import Address
from server.message import CommandInfo, Message
from server.message.operation import OPERATION

HOST = '127.0.0.1'
PORT = 5577
PASSWORD = 'P@$$w0rd'

log = logging.getLogger(__name__)


class AuthConnection:
    def __init__(self, connection: Connection, user: str = None, password: str = None) -> None:
        self.id = uuid4().hex
        self.connection = connection
        self.user = user
        self.password = password
        self.is_auth = False

    def is_ident(self) -> bool:
        return all((self.user, self.password))

    def ident(self):
        if not self.user:
            self.connection.send("User: ")
            return
        if not self.password:
            self.connection.send("Password: ")

    def fileno(self):
        return self.connection.fileno()

    def send(self, obj):
        self.connection.send(obj)

    def recv(self):
        return self.connection.recv()


class Connector:

    def __init__(self, message_router: callable):
        self._selector = selectors.DefaultSelector()
        self.clients = {}
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
        for client in self.clients:
            client['connection'].close()
        self.stop_event.set()
        self._accept_connection_thread.join()
        self.listener.close()

    def _accept(self, socket, mask):
        connection = AuthConnection(self.listener.accept())
        self.clients.update({connection.id: {'connection': connection, 'address': self.listener.last_accepted}})
        log.info(f'Client connected {self.listener.last_accepted}')
        connection.ident()
        self._selector.register(connection, selectors.EVENT_READ, self._on_message_received)

    def _on_message_received(self, connection, mask):
        recv = connection.recv()
        if recv[:6] == "USER: ":        # todo: separate auth logic
            connection.user = recv[6:]
        if recv[:10] == "PASSWORD: ":
            connection.password = recv[10:]
        if not connection.is_ident():
            connection.ident()
            return
        if not connection.is_auth:
            message = Message(
                -1,
                connection.id,
                CommandInfo(
                    -1,
                    OPERATION.Get_Token,  # 12 - GET_JWT
                    {
                        "user": connection.user,
                        "password": connection.password,
                    }
                )
            )
            connection.is_auth = True
            self.message_router(message)
            return

        # 3x int  game_id, object_id, operation_id
        (game_id, object_id, operation_id), args = unpack('3i', recv[:12]), recv[12:]
        try:
            args = json.loads(args.decode('utf-8'))
        except Exception as ex:
            log.exception(f'receive wrong format message {recv=} {ex=}')
            return
        if "jwt" not in args.keys():
            log.error(f'message without auth token rejected {operation_id=} {args=}')
            return

        message = Message(
            game_id=game_id,
            conn=connection.id,
            command_info=CommandInfo(
                object_id=object_id,
                operation=OPERATION(operation_id),
                args=args
            )
        )
        self.message_router(message)


class AuthServiceConnector:
    def __init__(self, auth_service_addr: Address, message_router: callable):
        self._host: str = auth_service_addr[0]
        self._port: int = auth_service_addr[1]
        self._pass: bytes = auth_service_addr[2]
        self._connection = Client((self._host, self._port), authkey=bytes(self._pass))
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._message_router = message_router
        self._process = threading.Thread(name="AuthConnectorThread", target=self.recv, daemon=True)

    def start(self):
        self._process.start()

    def stop(self):
        self._stop_event.set()
        self._process.join()

    def send(self, data: bytes):
        if self._stop_event.is_set():
            return

        try:
            with self._lock:
                self._connection.send(data)
                log.info(f"AuthConnector send {data}")
        except IOError as ex:
            log.error(f"AuthConnector sending failed: {data} {ex=}")  # Pass or Die

    def recv(self):
        while not self._stop_event.is_set():

            if not self._connection.poll():
                self._stop_event.wait(0.01)
                continue

            try:
                raw = self._connection.recv()
                mtype, data = unpack('i', raw[:4])[0], raw[4:]
                message = Message(-1, None, CommandInfo(-1, OPERATION(mtype), json.loads(data)))
                log.info(f"AuthConnector recv {message}")
            except IOError:
                log.error("AuthConnector recv failed")  # Pass or Die
            else:
                self._message_router(message)
