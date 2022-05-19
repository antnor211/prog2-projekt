import termcolor

class OptionInput():
    def __init__(self, mess, start, end):
        self._choice = -1

        while self._choice < start or self._choice > end:
            self._choice = input('\n[{}-{}] '.format(start, end) +
                           termcolor.colored(mess, 'green'))
            try:
                self._choice = int(self._choice)
            except:
                print('exception reached')
                break
    def getChoice(self):
        return self._choice