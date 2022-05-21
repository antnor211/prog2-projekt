import sqlite3
from server.database.Action import Action

from server.database.migrate import Migrate
from server.database.query import Query

class Database(Action):
    def __init__(self, db_path):
        Action.__init__(self, db_path)

    def handleMutation(self, mutationTuple, mutationType):
        self._cur.execute(self.q.mutations[mutationType], mutationTuple)
        self._con.commit()
        return mutationTuple

    def handleQuery(self, queryTuple, queryType):
        print(queryTuple)
        self._cur.execute(self.q.querys[queryType], queryTuple)

        rRows = self._cur.fetchall()
        return rRows

    def handleUpdate(self, udpateTuple, updateType):
        self._cur.execute(self.q.updates[updateType], udpateTuple)
        self._con.commit()
        return udpateTuple
    
    def handleDelete(self, mutationTuple, mutationType):
        self._cur.execute(self.q.deletes[mutationType], mutationTuple)
        self._con.commit()
        return mutationTuple
    def __enter__(self):
        return self

    def __exit__(self):
        pass