
from server.database.migrate import Migrate
from server.database.query import Query

class Database:
    def __init__(self):
        self.handleMigration = Migrate("database.db")
        self.handleQuery = Query("database.db")

    def __enter__(self):
        return self

    def __exit__(self):
        pass