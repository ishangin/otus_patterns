from enum import Enum, auto
from queue import Queue, Empty
import threading

from commands.worker import NewWorker, StopWorker, SoftStopWorker
from errors.exception_handler import ExceptionHandler
from interfaces.command import Command
from ioc.container import IoC


class STATUS (Enum):
    STOPPED = auto()
    RUNNING = auto()


class Worker:
    def __init__(self, worker_id: int, queue: Queue, ex_handler: ExceptionHandler):
        self.id = worker_id
        self.status = STATUS.STOPPED
        self._thread = threading.Thread(name=f'worker{self.id}', target=self.process)
        self._start_event = threading.Event()
        self._stop_event = threading.Event()
        self._soft_stop_event = threading.Event()
        self._queue = queue
        self._ex_handler = ex_handler

    def stop(self):
        self._stop_event.set()
        try:    # don't like for me. think about fix it
            self._thread.join()
        except RuntimeError:  # if _thread == current_thread
            pass
        self.status = STATUS.STOPPED

    def soft_stop(self):
        self._soft_stop_event.set()
        try:    # don't like for me. think about fix it.
            self._thread.join()
        except RuntimeError:  # if _thread == current_thread
            pass
        self.status = STATUS.STOPPED

    def start(self):
        self._thread.start()
        self._start_event.wait()
        self.status = STATUS.RUNNING

    def process(self) -> None:
        self._start_event.set()
        print(f'THREAD START {self._thread.name} : ID {self.id} : PID {threading.current_thread().ident}')

        while True:
            if self._stop_event.is_set():
                break
            try:
                cmd = self._queue.get(block=True, timeout=1)
            except Empty:
                if self._soft_stop_event.is_set():
                    print(
                        f'THREAD SOFT STOP {self._thread.name} : ID {self.id} : PID {threading.current_thread().ident}')
                    return
                else:
                    continue
            print(f'{self._thread.name} : ID {self.id} : PID {threading.current_thread().ident} : CMD {cmd}')
            try:
                cmd.execute()
            except Exception as ex:
                self._ex_handler.handle(cmd, ex)
        print(f'THREAD STOP {self._thread.name} : ID {self.id} : PID {threading.current_thread().ident}')


class Server:

    def __init__(self, queue: Queue):
        self._queue = queue
        self.ex_handler = ExceptionHandler(self._queue)
        self._workers = {0: Worker(worker_id=0, queue=self._queue, ex_handler=self.ex_handler)}  # first worker

    def spawn_worker(self):
        worker = Worker(len(self._workers), queue=self._queue, ex_handler=self.ex_handler)
        self._workers.update({len(self._workers): worker})
        worker.start()

    def stop_worker(self, worker_id: int, force: bool = False):
        if force:
            self._workers.get(worker_id).stop()
        else:
            self._workers.get(worker_id).soft_stop()
        self._workers.pop(worker_id)

    def start(self):
        for _, worker in self._workers.items():
            worker.start()

    def stop(self):
        for _, worker in self._workers.items():
            worker.stop()
        self._workers = {}

    def put_command(self, cmd: Command):
        self._queue.put(cmd)


IoC.resolve('IoC.Register', 'Worker.New', NewWorker).execute()
IoC.resolve('IoC.Register', 'Worker.Stop', StopWorker).execute()
IoC.resolve('IoC.Register', 'Worker.SoftStop', SoftStopWorker).execute()


# if __name__ == '__main__':
#     s = Server(Queue())
#     s.start()
#     s.put_command(LogWriter(ValueError('test')))
#     cmd = IoC.resolve('Worker.New', s)
#     s.put_command(cmd)
#     s.stop()
#     print('END')
