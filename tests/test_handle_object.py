from commands import LogWriter
from commands.handle_object import HandleObject
from ioc.container import GameCommand
from mtypes.vector import Vector
from objects import SpaceShip

obj_a = SpaceShip(position=Vector(50, 30), radius=10)
obj_b = SpaceShip(position=Vector(40, 60), radius=50)

game_objects = [obj_a, obj_b]
game = GameCommand()
[game.add_game_object(obj) for obj in game_objects]


class TestHandleObject:

    def test_handle_object(self):
        HandleObject(obj_a).execute()
        HandleObject(obj_b).execute()
        cmds = []
        while not game._queue.empty():
            cmd = game._queue.get()
            cmds.append(cmd)
            cmd.execute()

        log_cmd = [cmd for cmd in cmds if isinstance(cmd, LogWriter)]
        assert len(log_cmd) == 1
        assert 'are collided' in log_cmd[0]._ex.args[0]
