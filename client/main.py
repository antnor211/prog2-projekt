import sys
import os
import time

sys.path.append(os.getcwd())

from clientArgParser import ClientArgParser
from clientSocket import ClientSocket

if __name__ == '__main__':
    cap = ClientArgParser()
    targetIp = cap.getArguments().i
    targetPort = cap.getArguments().p

    with ClientSocket(targetIp, targetPort) as cs:
        while True:
            time.sleep(2) #test purposes
            cs.send({'test': 'test'})

