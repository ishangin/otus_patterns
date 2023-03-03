import json
import logging
import threading
from multiprocessing.connection import Listener
from struct import unpack, pack

from .auth import Auth
from models import Message, MessageType, User, Game
from db import GAMES

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

log = logging.getLogger(__name__)
HOST = 'localhost'
PORT = 5578
listener = Listener((HOST, PORT))


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
        message = Message(message_type, data)
        log.debug(f'Message received {message=}')
        match message.type:
            case MessageType.NEW_GAME:
                users = message.data.get('users')
                game_id = len(GAMES)
                game = GAMES.append({
                    'id': game_id,
                    'users': [Auth(User(u)).get_user().id for u in users]
                })
                self._connection.send(pack('2I', MessageType.RESPONSE, game_id))
            case MessageType.GET_JWT:
                user = User(login=message.data.get('user'),
                            password=message.data.get('password'))
                auth = Auth(user)
                auth.check_pass()
                if auth.user.authenticated:
                    game_id = message.data.get('game_id')
                    game = Game(**GAMES[int(game_id)])
                    jwt = auth.get_jwt(game)
                    if jwt:
                        self._connection.send(pack('I', MessageType.RESPONSE) + bytes(jwt.encode('UTF-8')))


if __name__ == '__main__':
    AuthService().start()
