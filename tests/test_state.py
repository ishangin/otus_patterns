from queue import Queue
from time import sleep

from commands.state import MoveToCommand, RunCommand
from server.server import Server
from server.modes import Normal, MoveTo


class TestWorkerCommands:

    def test_change_mode(self):
        q = Queue()
        s = Server()
        s.start()
        assert len(s._workers) == 1
        s.new_game(s._workers[0])
        assert isinstance(s._workers[0].mode.state, Normal)
        # switch to move_to state
        s.put_command(MoveToCommand(queue=q, worker=s._workers[0]), 0)
        sleep(2)
        assert isinstance(s._workers[0].mode.state, MoveTo)
        # switch to normal state
        s.put_command(RunCommand(worker=s._workers[0]), 0)
        sleep(2)
        assert isinstance(s._workers[0].mode.state, Normal)
        s.stop()
