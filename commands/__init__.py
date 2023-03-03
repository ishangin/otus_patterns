from commands.move import Move
from commands.rotate import Rotate
from commands.check_fuel import CheckFuel
from commands.log_writer import LogWriter
from commands.macro_command import MacroCommand
from commands.worker import NewWorker, StopWorker, SoftStopWorker
# from commands.scope import ScopeNew, ScopeSetCurrent
from commands.repeater import Repeater, DoubleRepeater
from commands.game import GameCommand

__all__ = [
    'Move',
    'Rotate',
    'CheckFuel',
    'LogWriter',
    'MacroCommand',
    'NewWorker', 'StopWorker', 'SoftStopWorker',
    'Repeater', 'DoubleRepeater',
    'GameCommand',
    # 'ScopeNew', 'ScopeSetCurrent',
]


# import pkgutil
#
# __all__ = []
# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     __all__.append(module_name)
#     _module = loader.find_module(module_name).load_module(module_name)
#     globals()[module_name] = _module
