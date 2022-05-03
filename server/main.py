import ssl
import sys
import os
import json
from tkinter import E

sys.path.append(os.getcwd())

from socketServer import SocketServer
from commands import Commands
from database.Database import Database
from server.database.migrate import Migrate


if __name__ == "__main__":
    with SocketServer("localhost", 8000) as ss:
        with Database("database.db")as db:
            comamnds = Commands(db)
            while True:
                connector, address = ss.accept()
                data = connector.recv(1024)
                try:
                    payload = json.loads(data.decode('utf-8'))
                    print('payload', payload)
                    response = comamnds.handleCommand(payload)
                    print('response', response)
                    connector.send(json.dumps(response).encode())
                except Exception as e:
                    print('exception', e)
                    pass
                finally:
                    connector.close()