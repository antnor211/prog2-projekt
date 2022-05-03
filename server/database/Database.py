from distutils.log import INFO, info
import sqlite3
from server.database.Action import Action

from server.database.migrate import Migrate
from server.database.query import Query
import server.database.queryStrings as q_strings

class Database(Action):
    def __init__(self, db_path):
        Action.__init__(self, db_path)

    def handle_migration(self, path):
        migration = Migrate(path)
        migration.migrate_data()

    def handle_mutation(self, info_dict):
        str_to_exec = q_strings.mutate[info_dict["command"]].format(
            info_dict["params"]
        )
        self._cur.execute(str_to_exec)

    def handle_update(self, info_dict):
        str_to_exec = q_strings.update[info_dict["command"]].format(
            info_dict["params"]
        )
        self._cur.execute(str_to_exec)

    def handle_fetch(self, info_dict):
        str_to_exec = q_strings.fetch[info_dict["command"]].format(
            info_dict["params"]
        )
        self._cur.execute(str_to_exec)


    def __enter__(self):
        return self

    def __exit__(self):
        pass