import random
import math
class BlackjackUtility:
    def __init__(self):
        pass
    def _getSuitString(self, suitVal):
            print('suitval', suitVal)
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
                uniqueCard = True

        cardValue = (r % 13) + 1
        if cardValue == 1:
            cardValue = 'A'
        elif cardValue == 11:
            cardValue = 'J'
        elif cardValue == 12:
            cardValue = 'Q'
        elif cardValue == 13:
            cardValue = 'K'
        card = {
            'suit': self._getSuitString(math.floor(r / 13)),
            'orderValue': (r % 13 + 1),
            'value': str(cardValue)
        }
        return card    

    def getTotal(self, cards):
        print('\n getting total')
        aceCount = 0 
        total = 0
        for card in cards:
            print(card)
            val = card['orderValue']
            if val > 10:
                total += 10
            elif val == 1:
                aceCount += 1
            else:
                total += val
        
        for i in range(0, aceCount):
            if (total + 11) > 21:
                total += 1
            else:
                total += 11
        
        return total 

    def getWinener(self, dealerTotal, playerTotal):
        print(dealerTotal, playerTotal)
        if dealerTotal > 21:
            return 'DEALER BUST'
        if dealerTotal > playerTotal:
            return 'DEALER WIN'
        if dealerTotal < playerTotal:
            return 'PLAYER WIN'
        if dealerTotal == playerTotal:
            return 'DRAW'