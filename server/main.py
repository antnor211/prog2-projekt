import sys
import os
import json

sys.path.append(os.getcwd())

from socketServer import SocketServer

if __name__ == "__main__":
    with SocketServer("localhost", 8000) as ss:
        while True:
            conn, addr = ss.accept()
            msg = conn.recv(1024)
            response = 'foo bar' #test purposes
            try: 
                payload = json.loads(msg.decode('utf-8'))
                print('payload', payload)
                print('response', response)
                conn.send(json.dumps(response).encode())
            except:
                pass
            finally:
                conn.close()