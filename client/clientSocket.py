import socket
import json

from utils.socketParent import SocketParent

class ClientSocket(SocketParent):
    def __init__(self, host, port):
        SocketParent.__init__(self, host, port)
    
    def _start(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
        except Exception as e:
            print(e)
    
    def _close(self):
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._sock.close()
    
    def send(self, p):
        try:
            self._start()
            data = json.dumps(p)
            response = None
            self._sock.send(data.encode())
            response = self._sock.recv(20480)
            response = json.loads(response.decode())
            print(response)
        except Exception as e:
            print(e)
        self._close()
        return response

    def __enter__(self):
        return self
    def __exit__(self, *exc_info):
        print('exiting')
        self._sock.shutdown(socket.SHUT_RDWR)
        SocketParent.__exit__(self, exc_info)
