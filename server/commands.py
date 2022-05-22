from hashlib import new
from operator import imod
import uuid
import json

from server.blackjackUtil import BlackjackUtility

class Commands():
    def __init__(self, database):
        self._db = database
        self._blackjackutil = BlackjackUtility()


    def login(self, command):
        username = command['body']['username']
        session = str(uuid.uuid4())
        if not username or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (username,), 'getUserByUsername')
        if len(userId) == 0:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        password = self._db.handleQuery((username), 'getPassword')[0][0]
        password = ''.join(password)
        if password != command['body']['password']:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        self._db.handleUpdate(
            (session, username), 'updateSession')
        player_balance = self._db.handleQuery((session,), 'getBalance')[0][0]
        return {
            'code': '200',
            'session': session,
            'playerBalance': player_balance,
        }

    def createUser(self, command):
        username = command['body']['username']
        password = command['body']['password']
        session = str(uuid.uuid4())

        if not username or not password:
            return({'code': '400', 'message': 'Missing Parameters'})
        print(username)
        userId = self._db.handleQuery(
            (username,), 'getUserByUsername')
        
        if len(userId) != 0:
            return({'code': '400', 'message': 'Username Taken'})
        self._db.handleMutation(
            [username, password, session, 100], 'createUser')

        return {
            'code': '200',
            'session': session,
            'playerBalance': 100
        }

    def deleteUser(self, command):
        username = "\'"+command['body']['username']+"\'"

        if not command['body']['username'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handle_query(
            username, 'getUserByUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        #session = self._db.handle_query(
        #    (userId[0][0],), 'getCurrentSession')
        #if session[0][0] != command['session']:
        #    return({'code': '401', 'message': 'No session established'})
        self._db.handle_deletion(
            username, 'deleteUser')
        return {
            'code': '200',
        }

    def newPassword(self, command):
        if not command['body']['username'] or not command['session'] or not command['body']['newPassword']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db. handle_query(
            (command['body']['username'],), ' getUserByUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db. handle_query(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleUpdate(
            (command['body']['newPassword'], userId[0][0],), 'newPassword')

        return {
            'code': '200',
        }

    def blackjackCreateGame(self, command):
        session = command['session']
        bet = command['body']['playerBet']
        if not session or not bet:
            return({'code': '400', 'message': 'Missing Parameters'})
        dealerCards = []
        playerCards = []
        for i in range(0, 2):
            dealerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        for i in range(0, 2):
            playerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        print(session)
        user = self._db.handleQuery(
            (session,), 'getUserBySession')[0]
        resultState = 'false'
        self._db.handleMutation(
            (user[4], json.dumps(playerCards).encode(), json.dumps(dealerCards).encode(), bet), 'blackjackCreateGame')
        if self._blackjackutil.getTotal(playerCards) == 21:
            resultState = 'BLACKJACK 21!'
            newTotal = playerBalance + bet * 2.5
            self._db.handleUpdate(
                (newTotal, session,), 'updatePlayerBalance')
            playerBalance = newTotal
            self._db.handleDelete(
                (session,), 'deleteGame')
        
        
        return {
            'code': '200',
            'gameSession': str(uuid.uuid4()),
            'game': {
                'dealer': {
                    'cards': dealerCards,
                    'total': self._blackjackutil.getTotal(dealerCards),
                },
                'player': {
                    'cards': playerCards,
                    'total': self._blackjackutil.getTotal(playerCards),
                },
                'resultState': resultState
            }
        }

    def blackjackHit(self, command):
        session = command['session']
        if not session:
            return({'code': '400', 'message': 'Missing Parameters'})
        #addCheck when db is up and running
        game = self._db.handleQuery(
            (session,), 'fetchGame')[0]
        playerCards = json.loads(game[2].decode('utf-8'))
        newCard = self._blackjackutil.getRandomCard(playerCards)
        print(newCard)
        playerCards.append(newCard)
        print('playerCards', playerCards)
        playerBalance = self._db.handleQuery(
                (session,), 'getBalance')[0][0]
        
        self._db.handleUpdate(
            (json.dumps(playerCards).encode(), session,), 'updatePlayerCards')
        
        bust = 'false'
        if self._blackjackutil.getTotal(playerCards) > 21:
            bust = 'PLAYER BUST'
            bet = game[4]
            newTotal = playerBalance - bet
            self._db.handleUpdate(
                (newTotal, session,), 'updatePlayerBalance')
            playerBalance = newTotal
            self._db.handleDelete(
                (session,), 'deleteGame')

        return {
                'code': '200',
                'gameSession': session,
                'head': 'blackjackHit',
                'game': {
                    'player': {
                        'cards': playerCards,
                        'total': self._blackjackutil.getTotal(playerCards),
                        'playerBalance': playerBalance
                    },
                    'resultState': bust
                }
            }

        
    def blackjackStand(self, command):
        session = command['session']
        if not session:
            return({'code': '400', 'message': 'Missing Parameters'}) 
        # TODO FIX hookup to db
        game = self._db.handleQuery(
            (session,), 'fetchGame')[0]
        playerCards = json.loads(game[2].decode('utf-8'))
        dealerCards = json.loads(game[3].decode('utf-8'))
        playerBalance = self._db.handleQuery(
                (session,), 'getBalance')[0][0]
        
        while self._blackjackutil.getTotal(dealerCards) < 17 :
            dealerCards.append(self._blackjackutil.getRandomCard(dealerCards))
        playerTotal = self._blackjackutil.getTotal(playerCards)
        dealerTotal = self._blackjackutil.getTotal(dealerCards)
        resultState = self._blackjackutil.getWinener(dealerTotal, playerTotal)
        if resultState == 'DEALER BUST' or resultState == 'PLAYER WIN':
            bet = game[4]
            newTotal = playerBalance + bet * 2
            self._db.handleUpdate(
                (newTotal, session,), 'updatePlayerBalance')
            playerBalance = newTotal
        elif resultState == 'DEALER WIN':
            bet = game[4]
            newTotal = playerBalance - bet 
            self._db.handleUpdate(
                (newTotal, session,), 'updatePlayerBalance')
            playerBalance = newTotal
        self._db.handleDelete(
                (session,), 'deleteGame')

        return {
                    'code': '200',
                    'gameSession': session,
                    'head': 'blackjackStand',
                    'game': {
                        'dealer': {
                            'cards': dealerCards,
                            'total': self._blackjackutil.getTotal(dealerCards),
                        },
                        'player': {
                            'cards': playerCards,
                            'total': self._blackjackutil.getTotal(playerCards),
                            'playerBalance': playerBalance,
                        },
                        'resultState': str(resultState)
                    }
                }
    def logout(self, command):
        if not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handle_query(
            (command['body']['username'],), ' getUserByUsername')
        if len(userId) == 0:
            return(
                {
                    'code': '400', 
                    'message': 'Username Does not match any records'
                }
                )
        self._db.handle_update(
            (str(uuid.uuid4()), userId[0][0]), 'session')

    def handleCommand(self, command):
        try:
            return getattr(self, command['head'])(command)
        except Exception as e:
            print('exception reached')
            print(e)
            return Exception


if __name__ == '__main__':
    pass

