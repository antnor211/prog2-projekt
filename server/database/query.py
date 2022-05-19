import sqlite3

from server.database.DBStrings import DBStrings

class Query:
    def __init__(self, db_path):
        self._db_path = db_path
        self._con = sqlite3.connect(self._db_path)
        self._cur = self._con.cursor()


    def create_user(self, username, password):
        query = DBStrings.mutate["create_user"].format(
            username = username, 
            password = password)
        print(query)
        self._cur.execute(query)
        self._con.commit()

    