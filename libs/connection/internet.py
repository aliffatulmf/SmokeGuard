import socket


def is_online():
    try:
        socket.create_connection(("1.1.1.1", 53), 5)
        return True
    except OSError:
        return False
