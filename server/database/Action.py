import sqlite3
from server.database.queryStrings import queryStrings

class Action:
    def __init__(self, path_database):
        self._path_database = path_database
        self._con = sqlite3.connect(self._path_database)
        self._cur = self._con.cursor()
        self.q = queryStrings()

    def commit_crud(self):
        self._con.commit()
        self._con.close()

    def handle_query(self, params, command):
        query = self.q.query(command).format(username=params)
        to_return = ""
        try:
            data = self._cur.execute(query)
            data = data.fetchall()
            to_return = data[0]
        except:
            to_return = ""
        return to_return
        
    def handle_mutation(self, params, command):
        query = self.q.query(command).format(
            username=params[0],
            password=params[1],
            session=params[2]
        )
        values = (params[0], params[1], params[2])
        print(query)
        try:
            print("got here")
            print(params)
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except:
            print("\nNÅGOT GICK INTE SOM DET SKULLE :(\n")
            
    def handle_update(self):
        pass