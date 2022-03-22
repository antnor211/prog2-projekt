class SocketParent:
    def __init__(self, host, port):
        self._host = host
        self._port = port
    def __exit__(self, exc_info):
        self.sock.close()
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)