import ssl
import sys
import os
import json

sys.path.append(os.getcwd())

from socketServer import SocketServer
from commands import Commands
from database.Database import Database
from server.database.migrate import Migrate
from server.serverArgParser import ServerArgParser


if __name__ == "__main__":

    cap = ServerArgParser()
    dbClean = cap.getArguments().c
    targetPort = cap.getArguments().p

    if dbClean:
        mig = Migrate("server/database/database.db")
        mig.migrateData()
    
    with SocketServer("localhost", targetPort) as ss:
        with Database("server/database/database.db")as db:
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