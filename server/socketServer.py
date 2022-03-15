import socket
import sys
import os

<<<<<<< HEAD:server/socetServer.py
class Server:
=======
from utils.socketParent import SocketParent

class SocketServer(SocketParent):
>>>>>>> 7fe4743bd6d476bfd7cd48ae8b146ecfca694680:server/socketServer.py
    def __init__(self, host, port):
        SocketParent.__init__(self, host, port)

    def __enter__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self._host, self._port))
        print('[*] Server running on {}'.format(self._port))
        s.listen(10)
        connector, address = s.accept()
        with connector:
            print(f"Connected to {address}")
            while True:
                data = connector.recv(1024)
                if not data:
                    break
                connector.sendall(data)
        self._sock = s

        return self._sock

    def __exit__(self, *exc_info):
        SocketParent.__exit__(self, exc_info)



