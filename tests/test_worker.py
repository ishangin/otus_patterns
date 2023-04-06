from queue import Queue
from time import sleep

import pytest

from commands.debug import EmptyCmd, SleepCmd
from commands.worker import NewWorker, StopWorker, SoftStopWorker
from errors.exception_handler import ExceptionHandler
from server.__main__ import Worker, Server


class FakeServer:
    spawn_worker = None
    stop_worker = None


class BrokenFakeServer:
    ...


class TestWorkerCommands:

    def test_new_worker(self, mocker):
        mocker.patch.object(FakeServer, 'spawn_worker')
        NewWorker(FakeServer).execute()
        FakeServer.spawn_worker.assert_called()
        FakeServer.spawn_worker.assert_called_once()
        FakeServer.spawn_worker.assert_called_once_with()

    def test_new_worker_exception(self, mocker):
        with pytest.raises(TypeError):
            NewWorker(FakeServer).execute()
        with pytest.raises(AttributeError):
            NewWorker(BrokenFakeServer).execute()

    def test_stop_worker(self, mocker):
        mocker.patch.object(FakeServer, 'stop_worker')
        StopWorker(FakeServer, 0).execute()
        FakeServer.stop_worker.assert_called()
        FakeServer.stop_worker.assert_called_once()
        FakeServer.stop_worker.assert_called_once_with(worker_id=0, force=True)

    def test_stop_worker_exception(self, mocker):
        with pytest.raises(TypeError):
            StopWorker(FakeServer, 0).execute()
        with pytest.raises(AttributeError):
            StopWorker(BrokenFakeServer, 0).execute()

    def test_soft_stop_worker(self, mocker):
        mocker.patch.object(FakeServer, 'stop_worker')
        SoftStopWorker(FakeServer, 0).execute()
        FakeServer.stop_worker.assert_called()
        FakeServer.stop_worker.assert_called_once()
        FakeServer.stop_worker.assert_called_once_with(worker_id=0, force=False)

    def test_soft_stop_worker_exception(self, mocker):
        with pytest.raises(TypeError):
            SoftStopWorker(FakeServer, 0).execute()
        with pytest.raises(AttributeError):
            SoftStopWorker(BrokenFakeServer, 0).execute()

    @pytest.mark.skip('change server start with auth service')
    def test_check_real_threads(self):
        s = Server()
        s.start()
        s.new_game(s._workers.get(0))
        assert len(s._workers) == 1

# hard stop worker test
        for _ in range(2):
            s.put_command(EmptyCmd(), 0)
        s.put_command(StopWorker(s, 0), 0)
        for _ in range(3):
            s.put_command(EmptyCmd(), 0)
        sleep(2)
        assert len(s._workers) == 0

# start worker test
        threads_count = len(s._workers)
        # s.spawn_worker()
        # s.put_command(NewWorker(s))
        NewWorker(s).execute()

        assert len(s._workers) == 1
        assert threads_count == len(s._workers) - 1
        s.games.update({0: s._workers[0]})
# soft stop worker test
        s.put_command(SleepCmd(1), 0)
        s.put_command(SoftStopWorker(s, 0), 0)
        for _ in range(3):
            s.put_command(EmptyCmd(), 0)
        sleep(3)
        assert len(s._workers) == 0

        s.stop()


class TestWorkerClass:

    def test_worker_start_stop(self, mocker):
        q = Queue()
        ex_handler = ExceptionHandler(queue=q)
        worker = Worker(worker_id=0, queue=q, ex_handler=ex_handler)
        mocker.patch.object(worker, "_worker_thread")
        mocker.patch.object(worker, "_start_event")
        mocker.patch.object(worker, '_stop_event')
        mocker.patch.object(worker, '_soft_stop_event')

        worker.start()
        worker._worker_thread.start.assert_called()
        worker._worker_thread.start.assert_called_once()
        worker._worker_thread.start.assert_called_once_with()
        worker._start_event.wait.assert_called()
        worker._start_event.wait.assert_called_once()
        worker._start_event.wait.assert_called_once_with()

        worker.stop()
        worker._worker_thread.join.assert_called()
        worker._worker_thread.join.assert_called_once()
        worker._worker_thread.join.assert_called_once_with()
        worker._stop_event.set.assert_called()
        worker._stop_event.set.assert_called_once()
        worker._stop_event.set.assert_called_once_with()

        # worker.start()
        # worker._thread.start.assert_called()

        worker.soft_stop()
        worker._worker_thread.join.assert_called()
        assert worker._worker_thread.join.call_count == 2
        assert worker._worker_thread.join.call_count == 2
        worker._soft_stop_event.set.assert_called()
        worker._soft_stop_event.set.assert_called_once()
        worker._soft_stop_event.set.assert_called_once_with()
