import logging
from server.__main__ import Server


FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == '__main__':
    s = Server(auth_service_addr=("127.0.0.1", 5578, bytes("P@$$w0rd", "UTF8")))
    s.start()
    s.stop()
