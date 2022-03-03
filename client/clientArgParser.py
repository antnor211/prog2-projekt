import sys
import os
from tokenize import String

sys.path.append(os.getcwd())
from utils.argParser import argParser

class clientArgParser(argParser):
    def __init__(self):
        argParser.__init__(self)
        self.parser.add_argument('-p', metavar='Port', type=int,
                        help='TCP port number to of Lorum Ipsum', required=True)
        self.parser.add_argument('-H', metavar='Host', type=str,
                        help='Host ip to Lorum Ipsum', required=True)
        self.loadArgs()

