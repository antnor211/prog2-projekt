from ssl import ALERT_DESCRIPTION_RECORD_OVERFLOW
import asciiArt
import time
import datetime
import termcolor
import os
import json
import socket
import re
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import argparse

from client.blackjack.blackjack import BlackJack

class ClientScope():
    def __init__(self, sock, username, password):
        self.currentFrame = None
        self._PreviousFrame = None
        self._socket = sock
        self._username = username
        self._password = password
        self._failedLogin = False

    def _optionInput(self, mess, start, end):
        choice = -1

        while choice < start or choice > end:
            choice = input('\n[{}-{}] '.format(start, end) +
                           termcolor.colored(mess, 'green'))
            try:
                choice = int(choice)
            except:
                break
        return choice

    def _page(self, title):
        os.system('clear')
        print(asciiArt.smallAppLogo + asciiArt.smallAppTitle)
        print(termcolor.colored('-'*10 + title + '-'*10, 'blue'))
        print('\n'*1)
    
    def _blackjackPage(self, playerCards, dealerCards, playerTotal, dealerTotal, result):
        os.system('clear')
        print(dealerCards)
        print('Dealer Total:', dealerTotal)
        print('\n'*3)
        print(termcolor.colored('-'*10 + ' BLACKJACK ' + '-'*10, 'blue'))
        print('\n'*5)
        print(playerCards)
        print('Your Total:', playerTotal)
        print('\n'*1)
        if result:
            color = 'green'
            if result == 'dealer win' or 'player bust':
                color = 'red'
            if result == 'draw':
                color = 'yellow'
            print(termcolor.colored('-'*10 + result + '-'*10, color))

    def loginMethod(self):
        self._page('LOGIN METHOD')
        print('[0] Login with existing account')
        print('[1] Create new account')

        choice = self._optionInput('Choose Option ', 0, 1)
        self.currentFrame = self.login if choice == 0 else self.createAccount
        self.currentFrame()
        return False

    def login(self):
        self._page('LOGIN')
        password = ''
        username = ''
        if self._username != '' and self._password != '' and not self._failedLogin:
            print(termcolor.colored(
                '[TRYING USERNAME AND PASSWORD IN CONFIG FILE]', 'green'))
            username = self._username
            password = self._password
            time.sleep(1)
        else:

            username = input('[Username] ')
            self._username = username.strip()
            if username or username == '':
                password = input('[Password] ')
        password = SHA256.new(data=password.strip().encode())
        p = {
            'head': 'login',
            'body': {
                'username': self._username,
                'password': password.hexdigest(),
            },
            'session': ''
        }
        response = self._socket.send(p)
        print('response', response)
        if response['code'] == '200':
            self._session = response['session']
            self.currentFrame = self.menu
        else:
            self._failedLogin = True
            print(termcolor.colored('[WRONG PASSWORD OR USERNAME]', 'red'))
            time.sleep(1)

    def createAccount(self):
        self._page('CREATE ACCOUNT')

        password = ''

        username = input('\r[Username] ')
        self._username = username.strip()
        if username or username == '':
            password = input('[Password] ')

        key = RSA.generate(2048)

        f = open('{}.pem'.format(self._username), 'wb')
        f.write(key.export_key('PEM'))
        f.close()
        pk = key.publickey().export_key()

        password = SHA256.new(data=password.strip().encode())

        p = {
            'head': 'create_user',
            'body': {
                'username': self._username,
                'password': password.hexdigest(),
                'publicKey': pk.decode(),
            },
            'session': ''
        }

        response = self._socket.send(p)
        if response['code'] == '200':
            self._session = response['session']
            self.currentFrame = self.menu

    def menu(self):
        self._page('MENU')
        print('[0] Play Blackjack')
        print('[1] Settings')
        choice = self._optionInput('Choose Option ', 0, 1)

        if choice == 0:
            self.currentFrame = self.blackjack
        elif choice == 1:
            self.currentFrame = self.settings

    def settings(self):
        self._page('SETTINGS')
        print('[0] Change Password')
        print('[1] Delete Account')
        choice = self._optionInput('Choose Option ', 0, 1)

        if choice == 0:
            self.currentFrame = self.changePassword
        elif choice == 1:
            self.currentFrame = self.deleteUser
    
    def blackjack(self): 
        gameInstance = BlackJack()
        p = {
            'head': 'blackjackCreateGame',
            'body': {
            },
            'session': self._session
        }

        createResponse = self._socket.send(p)
        
        if createResponse['code'] == '200':
            gameInstance.updateGameSession(createResponse['gameSession'])
            gameInstance.newDealerCards(createResponse['game']['dealer']['cards'])
            gameInstance.newPlayerCards(createResponse['game']['player']['cards'])
            gameInstance.newDealerTotal(createResponse['game']['dealer']['total'])
            gameInstance.newPlayerTotal(createResponse['game']['player']['total'])
        else: 
            self.currentFrame = self.menu

        actionResponse = None
        
        while True:
            if actionResponse:
                if actionResponse['code'] == '200' and actionResponse['head'] == 'blackjackHit':
                    gameInstance.newPlayerCards(actionResponse['game']['player']['cards'])
                    gameInstance.newPlayerTotal(actionResponse['game']['player']['total'])
                    if actionResponse['game']['resultState'] == 'bust':
                        gameInstance.newResult(actionResponse['game']['resultState'])
                
                if actionResponse['code'] == '200' and actionResponse['head'] == 'blackjackStand':
                    gameInstance.newDealerCards(actionResponse['game']['dealer']['cards'])
                    gameInstance.newDealerTotal(actionResponse['game']['dealer']['total'])
                    gameInstance.newResult(actionResponse['game']['resultState'])
                
                actionResponse = None
            self._blackjackPage(gameInstance.getFormattedPlayerCards(), gameInstance.getForamttedDealerCards(), gameInstance.getPlayerTotal(),  gameInstance.getDealerTotal(), gameInstance.getResult())
            if not gameInstance.getResult():
                print('[0] Hit')
                print('[1] Stand')
                
                choice = int(self._optionInput('Choose Option ', 0, 1))
                if choice != 0 and choice != 1:
                    continue
                p = {
                    'head': 'blackjackHit' if choice == 0 else 'blackjackStand',
                    'body': {
                        'gameSession': gameInstance.gameSession,
                    },
                    'session': self._session
                }
                actionResponse = self._socket.send(p)
            else: 
                print('[0] New Game')
                print('[1] Return To Main Menu')
                choice = int(self._optionInput('Choose Option ', 0, 1))
                if choice != 0 and choice != 1:
                    continue
                if choice == 0:
                    break
                if choice == 1:
                    self.currentFrame = self.menu
                    break


    def __enter__(self):
        self.currentFrame = self.loginMethod
        return self

    def __exit__(self, *exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
