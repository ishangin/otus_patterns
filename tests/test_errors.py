from queue import Queue

from commands.check_fuel import CheckFuel
from commands.repeater import Repeater, DoubleRepeater
from commands.log_writer import LogWriter
from commands.move import Move
from main import log
from commands.rotate import Rotate
from server import server
from server.server import Server
from errors.exception_handler import ExceptionHandler


SERVER = Server()

Q = Queue()

EX_HANDLER = ExceptionHandler(Q)


def fake_start(self):
    while not self._queue.empty():
        cmd = self._queue.get()
        try:
            cmd.execute()
        except Exception as ex:
            self.ex_handler.handle(cmd, ex)


class TestExceptionHandler:

    # Log_handler

    def test_log_handler_put(self, mocker, mockobj):
        mocker.patch.object(Q, 'put')
        EX_HANDLER.log_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        Q.put.assert_called()
        Q.put.assert_called_once()
        assert isinstance(Q.put.call_args[0][0], LogWriter)
        assert Q.put.call_args[0][0]._ex.args[0] == 'test exception'

    def test_log_handler_queue(self, mocker, mockobj):
        EX_HANDLER.log_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        cmd = Q.get(timeout=3)
        assert isinstance(cmd, LogWriter)
        assert cmd._ex.args[0] == 'test exception'

    def test_server_log_handler(self, mocker, mockobj_move):
        mocker.patch('main.log.exception')
        mocker.patch.object(server.Server, 'start', fake_start)
        SERVER.put_command(Rotate(mockobj_move))
        SERVER.start()
        log.exception.assert_called()
        log.exception.assert_called_once()
        assert isinstance(log.exception.call_args[0][0], AttributeError)
        assert log.exception.call_args[0][0].args[0] == 'type object \'MockObj_Move\' has no attribute \'direction\''

    # Repeater_handler

    def test_repeater_handler_put(self, mocker, mockobj):
        mocker.patch.object(Q, 'put')
        EX_HANDLER.repeater_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        Q.put.assert_called()
        Q.put.assert_called_once()
        assert isinstance(Q.put.call_args[0][0], Repeater)

    def test_repeater_handler_queue(self, mocker, mockobj):
        EX_HANDLER.repeater_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        cmd = Q.get(timeout=3)
        assert isinstance(cmd, Repeater)

    def test_server_repeater_handler(self, mocker, mockobj_move):
        mocker.patch('commands.repeater.Repeater.execute')
        mocker.patch.object(server.Server, 'start', fake_start)
        SERVER.put_command(CheckFuel(mockobj_move))
        SERVER.start()
        Repeater.execute.assert_called()

    # DoubleRepeater_handler

    def test_double_repeater_handler_put(self, mocker, mockobj):
        mocker.patch.object(Q, 'put')
        EX_HANDLER.double_repeater_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        Q.put.assert_called()
        Q.put.assert_called_once()
        assert isinstance(Q.put.call_args[0][0], DoubleRepeater)

    def test_double_repeater_handler_queue(self, mocker, mockobj):
        EX_HANDLER.double_repeater_handler(cmd=Rotate(mockobj), ex=ValueError('test exception'))
        cmd = Q.get(timeout=3)
        assert isinstance(cmd, DoubleRepeater)

    def test_server_double_repeater_handler(self, mocker, mockobj_rotate):
        mocker.patch('commands.repeater.DoubleRepeater.execute')
        mocker.patch.object(server.Server, 'start', fake_start)
        SERVER.put_command(Move(mockobj_rotate))
        SERVER.start()
        DoubleRepeater.execute.assert_called()

# todo: make test for default_handler
