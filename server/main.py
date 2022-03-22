import sys
import os
import json

sys.path.append(os.getcwd())

from socketServer import SocketServer
from commands import Commands

if __name__ == "__main__":
    with SocketServer("localhost", 8000) as ss:
        with Commands(None) as commands:
            while True:
                msg = ss.data
                if msg:
                    try:
                        payload = json.loads(msg.decode('utf-8'))
                        response = commands.handleCommand(payload)
                        print('payload', payload)
                        print('response', response)
                        ss.sock.conn.send(json.dumps(response).encode())
                    except:
                        pass
                    finally:
                        ss.sock.conn.close()