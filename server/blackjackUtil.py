from enum import unique
import random
import math
class BlackjackUtility:
    def __init__(self):
        pass
    def _getSuitString(self, suitVal):
            print(suitVal)
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
        print('entered', drawn)
        def _getRandomCard():
            return math.floor(random.random()*52)
        r = 0
        r = _getRandomCard()
        uniqueCard = False
        while not uniqueCard and len(drawn) != 0:
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
                if card['orderValue'] + suitVal == r:
                    r = _getRandomCard()
                    break
                print(uniqueCard)
                uniqueCard = True
            print('entered 1')

        cardValue = r % 4
        if r == 0:
            cardValue = 'A'
        elif r == 10:
            cardValue = 'J'
        elif r == 11:
            cardValue = 'Q'
        elif r == 12:
            cardValue = 'K'
        print(cardValue)
        card = {
            'suit': self._getSuitString(math.floor(r / 13)),
            'orderValue': r % 4,
            'value': str(cardValue)
        }
        return card    

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