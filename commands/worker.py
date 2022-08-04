from interfaces.command import Command


class NewWorker(Command):
    def __init__(self, server):  # todo: create server interface and use it as type for 'server' arg
        self._server = server

    def execute(self) -> None:
        self._server.spawn_worker()


class StopWorker(Command):
    def __init__(self, server: object, worker: int):
        self._server = server
        self._worker = worker

    def execute(self) -> None:
        self._server.stop_worker(worker_id=self._worker, force=True)


class SoftStopWorker(Command):
    def __init__(self, server: object, worker: int):
        self._server = server
        self._worker = worker

    def execute(self) -> None:
        self._server.stop_worker(worker_id=self._worker, force=False)
