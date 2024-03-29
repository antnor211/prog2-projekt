from client.blackjack.card import Card

class BlackJack: 
    def __init__(self):
        self._dealerCards = []
        self._playerCards = []

        self._playerTotal = 0
        self._dealerTotal = 0

        self._playerBet = 0
        self._result = False

    def getPlayerCards(self):
        return self._playerCards 
    
    def getDealerCards(self):
        return self._dealerCards
    
    def getPlayerTotal(self):
        return self._playerTotal
    
    def getDealerTotal(self):
        return self._dealerTotal
    
    def newDealerTotal(self, total):
        self._dealerTotal = total

    def newPlayerTotal(self, total):
        self._playerTotal = total
        
    def newPlayerCards(self, cards):
        self._playerCards = []
        for card in cards:
            newCard = Card(card).getCard()
            self._playerCards.append(newCard)
    
    def newDealerCards(self, cards):
        self._dealerCards = []
        for card in cards:
            newCard = Card(card).getCard()
            self._dealerCards.append(newCard)
    
    def newResult(self, result):
        self._result = result
    
    def getResult(self):
        return self._result
    
    def addPlayerBet(self, playerBet):
        self._playerBet = playerBet
    
    def getPlayerBet(self):
        return self._playerBet
    
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

