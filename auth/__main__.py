import json
import logging
import threading
from multiprocessing.connection import Listener
from struct import pack, unpack

from .auth import Auth
from .models import Message, MessageType, User

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

log = logging.getLogger(__name__)
HOST = 'localhost'
PORT = 5578
PASSWORD = "P@$$w0rd"
listener = Listener((HOST, PORT), authkey=bytes(PASSWORD, "UTF8"))


class AuthService:
    def __init__(self):
        self._connection = None
        self.stop_event = threading.Event()

    def _lost_connection(self):
        self.stop_event.set()
        log.error('Connection lost')
        raise ConnectionError('Connection lost')

    def start(self):
        log.debug(f'Start listening on {HOST}:{PORT}')
        self._connection = listener.accept()
        log.debug(f'Connected: {listener.last_accepted}')
        while not self.stop_event.is_set():
            try:
                if not self._connection.poll():
                    self.stop_event.wait(0.01)
                    continue
            except IOError:
                self._lost_connection()
            try:
                message = self._connection.recv()
            except (EOFError, IOError):
                self._lost_connection()
            else:
                self._message_received(message)

    def _message_received(self, message):
        # TODO: try except if can not unpack
        message_type, data = unpack('I', message[:4])[0], message[4:]
        # TODO: try except if json.loads failed
        data = json.loads(data.decode('utf-8'))
        message = Message(MessageType(message_type), data)
        log.debug(f'AuthService message received {message=}')
        match message.type:
            case MessageType.GET_JWT:
                user = User(login=message.data.get('user'),
                            password=message.data.get('password'))
                auth = Auth(user)
                auth.check_pass()
                if auth.user.authenticated:
                    jwt = auth.get_jwt()
                    if jwt:
                        data = {"id": message.data["id"], "user_id": auth.user.id, "jwt": jwt}
                    else:
                        # todo: need auth status success or failed in message format
                        data = {"id": message.data["id"], "jwt": "error get jwt"}
                else:
                    data = {"id": message.data["id"], "jwt": "invalid user or password"}

                self._connection.send(pack('I', MessageType.RESPONSE.value) + bytes(json.dumps(data), "UTF8"))


if __name__ == '__main__':
    AuthService().start()
