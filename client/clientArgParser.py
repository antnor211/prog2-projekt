from utils.argParser import ArgParser

<<<<<<< HEAD
sys.path.append(os.getcwd())
from utils.argParser import argParser

class ClientArgParser(argParser):
=======
class ClientArgParser(ArgParser):
>>>>>>> 7fe4743bd6d476bfd7cd48ae8b146ecfca694680
    def __init__(self):
        ArgParser.__init__(self)
        self.parser.add_argument('-p', metavar='Port', type=int,
                        help='TCP port number to of Lorum Ipsum', required=True)
        self.parser.add_argument('-i', metavar='Host', type=str,
                        help='Host ip to Lorum Ipsum', required=True)
        self.loadArgs()

