import argparse

class ArgParser:
    def __init__(self):
       self.parser = argparse.ArgumentParser(description='Berzan Blackjack')
    
    def loadArgs(self):
        self.inputArguments = self.parser.parse_args()

    def getArguments(self):
        return self.inputArguments
