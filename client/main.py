import sys
import os
import time

sys.path.append(os.getcwd())
from clientConfig import ClientConfig
from clientArgParser import ClientArgParser
from clientSocket import ClientSocket
from clientScope import ClientScope

if __name__ == '__main__':
    
    conf = ClientConfig()
    cap = ClientArgParser()
    targetIp = cap.getArguments().i
    targetPort = cap.getArguments().p

    with ClientSocket(targetIp, targetPort) as clientSocket:
        with ClientScope(clientSocket, conf.readAttribute('username'), conf.readAttribute('password')) as clientScope:
            while True:
                clientScope.currentFrame()

