import termcolor

from client.blackjack.suitASCII import suits

class Card():
    def __init__(self, card):
        self._suit = card['suit']
        self._value = card['value']
        self._order = card['orderValue']
        self._cardString = suits[ self._suit].format( self._value if  self._value != '10' else 'X',  self._value if  self._value != '10' else 'X')
        self._color = None

    def _getValue(self):
        if self._value == 'A':
            return None
        try:
            val = int(self._value)
            return val
        except:
            return 10

    def _getColor(self):
        if self._suit == 'hearts':
            self._color = 'red'
        elif self._suit == 'spades':
            self._color = 'blue'
        elif self._suit == 'diamonds':
            self._color = 'green'
        elif self._suit == 'clubs':
            self._color = 'yellow'
        return self._color

    def _getColorChopped(self):
        splits = self._cardString.split('\n')
        colored = [termcolor.colored(part, self._color) for part in splits]
        return colored

    def getCard(self):
        return {
            'suit': self._suit,
            'value': self._getValue(),
            'cardString': self._cardString,
            'color': self._getColor(),
            'cardColoredChopped': self._getColorChopped()
        }

#test 
if __name__ == "__main__":
    c1 = Card('hearts', 5).getCard()
    c2 = Card('spades', 10).getCard()
    c3 = Card('clubs', 'K').getCard()
    c4 = Card('diamonds', 'A').getCard()
    print(termcolor.colored(c1['cardString'], c1['color']))
    print(termcolor.colored(c2['cardString'], c2['color']))
    print(termcolor.colored(c3['cardString'], c3['color']))
    print(termcolor.colored(c4['cardString'], c4['color']))
    print(c1['cardColoredChopped'])
