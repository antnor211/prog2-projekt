import re

class ClientConfig:
    def __init__(self):
        self._config = {
            'username': '',
            'password': ''
        }

        try:
            f = open('config.txt').readlines()
            username = re.split(r'username:', f[0][:-1])
            password = re.split(r'password:', f[1][:-1])
            if len(username) != 1:
                self._config['username'] = username[-1]
            else:
                self._config['username'] = ''
            if len(password) != 1:
                self._config['password'] = password[-1]
            else:
                self._config['password'] = ''
            f.close()
        except:
            pass

    def readAttribute(self, attribute):
        try:
            return self._config[attribute]
        except: 
            pass