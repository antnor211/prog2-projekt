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
            'head': 'createUser',
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
        print('[0] Send a Message')
        print('[1] Inbox')
        print('[2] Settings')
        choice = self._optionInput('Choose Option ', 0, 2)

        if choice == 0:
            self.currentFrame = self.sendMessage
        elif choice == 1:
            self.currentFrame = self.inbox
        elif choice == 2:
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

    def __enter__(self):
        self.currentFrame = self.loginMethod
        return self

    def __exit__(self, *exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
