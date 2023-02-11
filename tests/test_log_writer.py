import pytest

import commands
from commands.log_writer import LogWriter, log


class FakeLog:
    """
    haven't methods to write logs indo(), debug(), warning(), exception() etc
    will raise AttributeError exception when try call this methods
    """
    ...


class TestLogWriter:

    def test_log_writer(self, mocker):
        mocker.patch('commands.log_writer.log.exception')
        ex = ValueError('test ValueError exception')
        try:
            raise ex
        except Exception:
            LogWriter(ex).execute()

        log.exception.assert_called_once_with(ex)

    def test_log_writer_error(self, mocker):
        mocker.patch.object(commands.log_writer, 'log', FakeLog())
        ex = ValueError('test ValueError exception')
        try:
            raise ex
        except Exception:
            with pytest.raises(AttributeError):
                LogWriter(ex).execute()
