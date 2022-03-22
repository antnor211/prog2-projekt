from contextlib import nullcontext
import socket


from utils.socketParent import SocketParent

class SocketServer(SocketParent):
    def __init__(self, host, port):
        self.data = 'None'
        SocketParent.__init__(self, host, port)

    def __enter__(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self._host, self._port))
        print('[*] Server running on {}'.format(self._port))
        s.listen(10)
        self.connector, self.address = s.accept()

        with self.connector:
            print(f"Connected to {self.address}")
            while True:
                self.data = self.connector.recv(1024)
                if not self.data:
                    break
                self.connector.sendall(self.data)
            self.data = None
        self.sock = s

        return self

    def __exit__(self, *exc_info):
        SocketParent.__exit__(self, exc_info)



