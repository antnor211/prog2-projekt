
from server.database.migrate import Migrate
from server.database.query import Query

class Database:
    def __init__(self):
        self.handleMigration = Migrate()
        self.handleQuery = Query()
