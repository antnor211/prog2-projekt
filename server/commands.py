from operator import imod
import uuid
import database.queryStrings as q_strings
from server.blackjackUtil import BlackjackUtility

class Commands():
    def __init__(self, database):
        self._db = database
        self._blackjackutil = BlackjackUtility()

    def create_user(self, command):
        info_dict = {
            "command": "create_user",
            "params": 
            #[command["body"]["firstname"], 
            #command["body"]["lastname"], 
            [command["body"]["username"], 
            command["body"]["password"]]
        }
        return info_dict

    def delete_user(self, command):
        info_dict = {
            "command": "delete_user",
            "params": command["body"]["username"]
        }
        return info_dict

    def login(self, command):

        if not command['body']['username'] or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})

        # userId = self._db.handleQuery(
        #     (command['body']['username'],), 'getUserbyUsername')
        # if len(userId) == 0:
        #     return({
        #         'code': '401',
        #         'message': 'Username or password is incorrect'
        #     })
        # password = self._db.handleQuery((userId[0][0],), 'getPassword')
        # if password[0][0] != command['body']['password']:
        #     return({
        #         'code': '401',
        #         'message': 'Username or password is incorrect'
        #     })
        # newSess = self._db.handleUpdate(
        #     (str(uuid.uuid4()), userId[0][0]), 'session')

        return {
            'code': '200',
            'session': str(uuid.uuid4()), #newSess[0],
        }

    def createUser(self, command):
        print("här!!!!!")
        if not command['body']['username'] or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) != 0:
            return({'code': '400', 'message': 'Username Taken'})
        mResponse = self._db.handleMutation(
            (command['body']['username'], str(uuid.uuid4()), command['body']['password']), 'create_user')
        newSess = self._db.handleUpdate(
            (str(uuid.uuid4()), mResponse[1]), 'session')
        return {
            'code': '200',
            'session': newSess[0],
        }

    def deleteUser(self, command):
        if not command['body']['username'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleMutation(
            (userId[0][0],), 'deleteUser')

        return {
            'code': '200',
        }

    def newPassword(self, command):
        if not command['body']['username'] or not command['session'] or not command['body']['newPassword']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleUpdate(
            (command['body']['newPassword'], userId[0][0],), 'newPassword')

        return {
            'code': '200',
        }

    def blackjackCreateGame(self, command):
        if not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        dealerCards = []
        playerCards = []
        for i in range(0, 2):
            dealerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        for i in range(0, 2):
            playerCards.append(self._blackjackutil.getRandomCard(dealerCards + playerCards))
        # userId = self._db.handleQuery(
        #     (command['session'],), 'getUserBySession')
        #mResponse = self._db.handleMutation(
        #    (userId, str(uuid.uuid4()), dealerCards, playerCards ), 'blackjackCreateGame')

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
        playerCards = []
        newCard = self._blackjackutil.getRandomCard(playerCards)
        playerCards.append(newCard)
        print(newCard)
        return {
                'code': '200',
                'gameSession': sessionId,
                'head': 'blackjackHit',
                'game': {
                    'player': {
                        'newCard': newCard,
                        'total': self._blackjackutil.getTotal(playerCards),
                    }
                }
            }
    def blackjackStand(self, command):
        if not command['body']['gameSession'] and not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'}) 
        sessionId = command['body']['gameSession']
        #FIX hookup to db
        dealerCards = []
        playerCards = []
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
                        }
                    }
                }
    def logout(self, command):
        if not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        self._db.handleUpdate(
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

