import sqlite3
from server.database.DBStrings import DBStrings

class Action:
    def __init__(self, path_database):
        self._path_database = path_database
        self._con = sqlite3.connect(self._path_database)
        self._cur = self._con.cursor()
        self.q = DBStrings()

    def commit_crud(self):
        self._con.commit()
        self._con.close()