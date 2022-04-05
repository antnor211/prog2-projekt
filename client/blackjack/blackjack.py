from client.blackjack.card import Card

class BlackJack: 
    def __init__(self):
        self._dealerCards = []
        self._playerCards = []

        self._playerTotal = 0
        self._dealerTotal = 0
    
    def getDealerTotal(self):
        aceCount = 0 
        for card in self._dealerCards:
            val = card['value']
            if val:
                self._dealerTotal += val
            else:
                aceCount += 1
        
        for i in range(0, aceCount):
            if (self._dealerTotal + 11) > 21:
                self._dealerTotal += 1
            else:
                self._dealerTotal += 11
        
        return self._dealerTotal

    def getPlayerTotal(self):
        aceCount = 0 

        for card in self._playerCards:
            val = card['value']
            if val:
                self._playerTotal += val
            else:
                aceCount += 1
        
        for i in range(0, aceCount):
            if (self._playerTotal + 11) > 21:
                self._playerTotal += 1
            else:
                self._playerTotal += 11
        
        return self._playerTotal

    def getPlayerCards(self):
        return self._playerCards 
    
    def getDealerCards(self):
        return self._dealerCards
    
    def addPlayerCard(self, card):
        newCard = Card(card['suit'], card['value']).getCard()
        self._playerCards.append(newCard)
    
    def addDealerCard(self, card):
        newCard = Card(card['suit'], card['value']).getCard()
        self._dealerCards.append(newCard)

    def getFormattedPlayerCards(self):
        cardsString = ''
        for line in range(0, 7):
            for card in self._playerCards:
                 cardsString += card['cardColoredChopped'][line]
            cardsString += '\n'
        return cardsString

    def getForamttedDealerCards(self):
        cardsString = ''
        for line in range(0, 7):
            for card in self._dealerCards:
                cardsString += card['cardColoredChopped'][line]
            cardsString += '\n'
        return cardsString
    def updateGameSession(self, session):
        self.gameSession = session
#test
if __name__ == "__main__":
    b = BlackJack()
    b.addDealerCard({'suit': 'spades', 'value': 'K'})
    b.addDealerCard({'suit': 'hearts', 'value': 'K'})
    b.addDealerCard({'suit': 'hearts', 'value': 'A'})
    b.addDealerCard({'suit': 'hearts', 'value': 'A'})
    print(b.getDealerTotal())

