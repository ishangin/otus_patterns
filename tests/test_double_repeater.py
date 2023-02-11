import pytest

from Interfaces.command import Command
from commands.repeater import DoubleRepeater


class Cmd(Command):
    def execute(self) -> None:
        ...


class Fake_Cmd:
    """
    haven't method execute()
    will raise AttributeError exception when try call this method
    """
    ...


class TestRepeater:

    def test_double_repeater(self, mocker):
        cmd = Cmd()
        mocker.patch.object(cmd, 'execute')
        DoubleRepeater(cmd).execute()
        cmd.execute.assert_called()
        cmd.execute.assert_called_once()
        cmd.execute.assert_called_once_with()

    def test_double_repeater_error(self, mocker):
        with pytest.raises(AttributeError):
            DoubleRepeater(Fake_Cmd()).execute()
