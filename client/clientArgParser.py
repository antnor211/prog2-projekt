from utils.argParser import ArgParser

sys.path.append(os.getcwd())
from utils.argParser import argParser

class ClientArgParser(ArgParser):
    def __init__(self):
        ArgParser.__init__(self)
        self.parser.add_argument('-p', metavar='Port', type=int,
                        help='TCP port number to of Lorum Ipsum', required=True)
        self.parser.add_argument('-i', metavar='Host', type=str,
                        help='Host ip to Lorum Ipsum', required=True)
        self.loadArgs()

