from enum import unique
import random
import math
class BlackjackUtility:
    def __init__(self):
        pass
    def _getSuitString(self, suitVal):
            s = ''
            if suitVal == 0:
                s = 'hearts'
            elif suitVal == 1:
                s = 'spades'
            elif suitVal == 2:
                s = 'diamonds'
            elif suitVal == 3:
                s = 'clubs'
            return s
    def getRandomCard(self, drawn):
        def _getRandomCard():
            return math.floor(random.ranodm()*54)
        r = 0
        uniqueCard = False
        while not uniqueCard:
            r = _getRandomCard()
            for card in drawn:
                suitVal = 0
                if card['suit'] == 'hearts':
                    suitVal = 0
                elif card['suit'] == 'spades':
                    suitVal = 13
                elif card['suit'] == 'diamonds':
                    suitVal = 26
                elif card['suit'] == 'clubs':
                    suitVal = 39
                if card['value'] + suitVal == r:
                  break
                uniqueCard = True
        card = {
            'suit': self._getSuitVal(math.floor(r / 4)),
            'value': r % 4
        }
                



    def getTotal(self, cards):
        aceCount = 0 
        total = 0
        for card in cards:
            val = card['value']
            if val:
                total += val
            else:
                aceCount += 1
        
        for i in range(0, aceCount):
            if (total + 11) > 21:
                total += 1
            else:
                total += 11
        return total 

    def getWinner(self, dealerTotal, playerTotal):
        if playerTotal > 21:
            return 'bust'
        if dealerTotal > 21:
            return 'dealer bust'
        if dealerTotal > playerTotal:
            return 'dealer win'
        if dealerTotal < playerTotal:
            return 'player win'
        if dealerTotal == playerTotal:
            return 'draw' 