from re import U
import sqlite3

class Action:
    def __init__(self, path_database):
        self._path_database = path_database
        self._con = sqlite3.connect(self._path_database)
        self._cur = self._con.cursor()

    def create_user(self, firstname, lastname, username, password):
        query = """
        insert into users(firstname, lastname, username, password),
        ({firstname}, {lastname}, {username}, {password});
        """.format(firstname = firstname, lastname = lastname, username = username, password = password)
        print(query)
        self._cur.execute(query)

    def commit_crud(self):
        self._con.commit()
        self._con.close()