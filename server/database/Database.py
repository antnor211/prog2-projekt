import sqlite3

from server.database.migrate import Migrate
from server.database.query import Query
import server.database.queryStrings as q_strings

class Database:
    def __init__(self, db_path):
        self._db_path = db_path
        self._con = sqlite3.connect(self._db_path)
        self._cur = self._con.cursor()
        #self.handleMigration = Migrate("database.db")
        #self.handleQuery = Query("database.db")

    def handle_migration(self, path):
        migration = Migrate(path)
        migration.migrate_data()

    def handle_mutation(self, info_dict):
        str_to_exec = q_strings[info_dict["command"]].format(
            info_dict["params"][0],
            info_dict["params"][1],
            info_dict["params"][2],
            info_dict["params"][3]
        )
        self._cur.execute(str_to_exec)

    
    def __enter__(self):
        return self

    def __exit__(self):
        pass