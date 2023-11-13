import socket

from libs.logger.default import *


class INet:
    def __init__(self):
        pass

    def is_online(self) -> bool:
        try:
            socket.create_connection(("1.1.1.1", 53), 5)
            return True
        except OSError:
            return False
