import socket

class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

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
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()


if __name__ == "__main__":
    server = Server("localhost", 8000)
    server.__enter__()
