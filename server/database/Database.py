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
    
    def handle_session_query(self, params, command):
        query = self.q.query(command).format(session=params)
        to_return = ""
        try:
            data = self._cur.execute(query)
            data = data.fetchall()
            print(data)
            to_return = list(data[0])
            print('hanged')
            print(f"\n{data[0]}\n")
        except:
            to_return = ""
        return to_return

        
    def handle_mutation(self, params, command):
        query = self.q.query(command).format(
            username=params[0],
            password=params[1],
            session=params[2],
            balance=params[3]
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
        query = self.q.query(command).format(session=params[0], username=params[1])
        try:
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except:
            print("\nSomething went wrong\n")

    def handle_mutation_bj(self, params, command):
        print('session', params[0])
        query = self.q.query(command).format(
            session=params[0], 
            playerCards=params[1], 
            dealerCards=params[2]
            )
        try:
            self._cur.execute(query)
            self._con.commit()
            print("done")
        except Exception as e:
            print(e)
            print("\nSomething went wrong\n")


    def __enter__(self):
        return self

    def __exit__(self):
        pass