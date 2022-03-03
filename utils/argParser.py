import argparse

class argParser:
    def __init__(self):
       self.parser = argparse.ArgumentParser(description='Lorum Ipsum')
    
    def loadArgs(self):
        self.inputArguments = self.parser.parse_args()

    def getArguments(self):
        
        return self.inputArguments
