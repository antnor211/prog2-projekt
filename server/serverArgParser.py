from utils.argParser import ArgParser


class ServerArgParser(ArgParser):
    def __init__(self):
        ArgParser.__init__(self)
        self.parser.add_argument('-p', metavar='Port', type=int,
                        help='TCP port number to of Berzan Blackjack', required=True)
        self.parser.add_argument('-c', action='store_true',
                        help='Clean the database ')
        self.loadArgs()

