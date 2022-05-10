import sqlite3
from server.database.Action import Action

from server.database.migrate import Migrate
from server.database.query import Query
import server.database.queryStrings as q_strings

class Database(Action):
    def __init__(self, db_path):
        Action.__init__(self, db_path)


    def handle_query(self, params, command):
        query = self.q.query(command).format(username=params)
        to_return = ""
        try:
            data = self._cur.execute(query)
            data = data.fetchall()
            to_return = data[0]
            print(f"\n{data[0]}\n")
        except:
            to_return = ""
        return to_return
        
    def handle_mutation(self, params, command):
        query = self.q.query(command).format(
            username=params[0],
            password=params[1],
            session=params[2]
        )
        #values = (params[0], params[1], params[2])
        #print(query)
        try:
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except:
            print("\nSomething went wrong\n")
            
    def handle_deletion(self, params, command):
        query = self.q.query(command).format(username=params)
        try:
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except:
            print("\nSomething went wrong\n")
    
    def handle_update(self, params, command):
        query = self.q.query(command).format(username=params[0], session=params[1])
        try:
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except:
            print("\nSomething went wrong\n")


    def __enter__(self):
        return self

    def __exit__(self):
        pass