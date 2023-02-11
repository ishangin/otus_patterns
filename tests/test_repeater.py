import pytest

from Interfaces.command import Command
from commands.repeater import Repeater


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

    def test_repeater(self, mocker):
        cmd = Cmd()
        mocker.patch.object(cmd, 'execute')
        Repeater(cmd).execute()
        cmd.execute.assert_called()
        cmd.execute.assert_called_once()
        cmd.execute.assert_called_once_with()

    def test_repeater_error(self, mocker):
        with pytest.raises(AttributeError):
            Repeater(Fake_Cmd()).execute()
