from queue import Queue

from interfaces.command import Command
import ioc.container
from objects import Space


class GameCommand(Command):
    def __init__(self):
        self._queue = Queue()
        self._game_objects = []
        self._battle_field = Space()
        ioc.container.IoC.resolve('Scope.New', 0).execute()  # 0 args is root scope is parent for new game
        self._scope = ioc.container.IoC.scopes.current_scope
        ioc.container.IoC.resolve('IoC.Register', 'Queue', self._get_game_queue).execute()
        ioc.container.IoC.resolve('IoC.Register', 'GameObjects', self._get_game_objects).execute()
        ioc.container.IoC.resolve('IoC.Register', 'BattleField', self._get_battle_field).execute()
        # s.games.update({len(s.games): self._queue})

    def _get_game_objects(self):
        return self._game_objects

    def _get_battle_field(self):
        return self._battle_field

    def _get_game_queue(self):
        return self._queue

    def execute(self) -> None:
        command = self._queue.get(timeout=1)
        if command:
            ioc.container.IoC.resolve('Scope.SetCurrent', self._scope.id).execute()
            command.execute()
