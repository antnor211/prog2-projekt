from contextlib import nullcontext
import socket


from utils.socketParent import SocketParent

class SocketServer(SocketParent):
    def __init__(self, host, port):
        self.data = 'None'
        SocketParent.__init__(self, host, port)

    def __enter__(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen(10)
        self.sock = sock
        print('[*] Server running on {}'.format(self._port))
        return self.sock

        return self
    def clearData(self):
        self.data = None

    def __exit__(self, *exc_info):
        SocketParent.__exit__(self, exc_info)



