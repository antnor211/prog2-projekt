import sqlite3

class Action:
    def __init__(self, path_database):
        self._path_database = path_database
        self._con = sqlite3.connect(self._path_database)
        self._cur = self._con.cursor()