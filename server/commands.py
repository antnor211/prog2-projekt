from hashlib import new
from operator import imod
import uuid
import json

from requests import session
import database.queryStrings as q_strings
from server.blackjackUtil import BlackjackUtility

class Commands():
    def __init__(self, database):
        self._db = database
        self._blackjackutil = BlackjackUtility()


    def login(self, command):
        username = "\'"+command['body']['username']+"\'"
        new_sess = "\'"+str(uuid.uuid4())+"\'"
        if not command['body']['username'] or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handle_query(
            username, 'get_user_by_username')
        if len(userId) == 0:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        password = self._db.handle_query(username, 'get_password')
        password = ''.join(password)
        if password != command['body']['password']:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        self._db.handle_update(
            (new_sess, username), 'update_session')

        player_balance = self._db.handle_query(username, 'get_balance')
        print('got here 1')
        player_balance = ''.join(str(player_balance[0]))
        trimed_sess = self._db.trim_string(new_sess)
        print('got here 2')

        return {
            'code': '200',
            'session': trimed_sess,
            'playerBalance': player_balance,
        }

    def createUser(self, command):
        username = "\'" + command['body']['username'] + "\'"
        password = "\'" + command['body']['password'] + "\'"
        session = "\'"+str(uuid.uuid4())+"\'"

        if not command['body']['username'] or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})
        user_id = self._db.handle_query(
            username, 'get_user_by_username')
        if len(user_id) != 0:
            return({'code': '400', 'message': 'Username Taken'})
        self._db.handle_mutation(
            [username, password, session, 100], 'create_user')
        new_sess_tuple = self._db.handle_query(
            username, 'get_user_by_username')
        new_sess = list(new_sess_tuple)
        return {
            'code': '200',
            'session': new_sess[4],
            'playerBalance': 100
        }

    def deleteUser(self, command):
        username = "\'"+command['body']['username']+"\'"

        if not command['body']['username'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handle_query(
            username, 'get_user_by_username')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        #session = self._db.handle_query(
        #    (userId[0][0],), 'getCurrentSession')
        #if session[0][0] != command['session']:
        #    return({'code': '401', 'message': 'No session established'})
        self._db.handle_deletion(
            username, 'delete_user')
        return {
            'code': '200',
        }

    def newPassword(self, command):
        if not command['body']['username'] or not command['session'] or not command['body']['newPassword']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db. handle_query(
            (command['body']['username'],), ' get_user_by_username')
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
        session = "\'"+command['session']+"\'"
        if not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        dealerCards = []
        playerCards = []
        for i in range(0, 2):
            dealerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        for i in range(0, 2):
            playerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        print(session)
        user = self._db.handle_session_query(
            session, 'get_user_by_session')
        print(user)
        #load payload = json.loads(data.decode('utf-8'))
        #send json.dumps(response).encode()
        self._db.handle_mutation_bj(
            [user[4], json.dumps(playerCards).encode(), json.dumps(dealerCards).encode()], 'blackjack_create_game')
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
                }
            }
        }

    def blackjackHit(self, command):
        if not command['body']['gameSession'] and not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        sessionId = command['body']['gameSession']
        #addCheck when db is up and running
        game = self._db.handle_session_query(
            sessionId, 'fetch_game')
        print(game)
        playerCards = self._db.handle_session_query(
            session, 'get_user_by_session')
        newCard = self._blackjackutil.getRandomCard(playerCards)
        playerCards.append(newCard)
        bust = 'PLAYER BUST' if self._blackjackutil.getTotal(playerCards) > 21 else 'false'
        print(newCard)
        return {
                'code': '200',
                'gameSession': sessionId,
                'head': 'blackjackHit',
                'game': {
                    'player': {
                        'cards': playerCards,
                        'total': self._blackjackutil.getTotal(playerCards),
                    },
                    'resultState': bust
                }
            }

        
    def blackjackStand(self, command):
        if not command['body']['gameSession'] and not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'}) 
        sessionId = command['body']['gameSession']
        # TODO FIX hookup to db
        dealerCards = []
        playerCards = []
        while self._blackjackutil.getTotal(dealerCards) <= 17 :
            dealerCards.append(self._blackjackutil.getRandomCard(dealerCards))
        playerTotal = self._blackjackutil.getTotal(playerCards)
        dealerTotal = self._blackjackutil.getTotal(dealerCards)
        resultState = self._blackjackutil.getWinener(dealerTotal, playerTotal)
        
        return {
                    'code': '200',
                    'gameSession': sessionId,
                    'head': 'blackjackStand',
                    'game': {
                        'dealer': {
                            'cards': dealerCards,
                            'total': self._blackjackutil.getTotal(dealerCards),
                        },
                        'player': {
                            'cards': playerCards,
                            'total': self._blackjackutil.getTotal(playerCards),
                        },
                        'resultState': str(resultState)
                    }
                }
    def logout(self, command):
        if not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handle_query(
            (command['body']['username'],), ' get_user_by_username')
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

