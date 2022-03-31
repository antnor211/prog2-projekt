
from migrate import Migrate
from query import Query

class Database:
    def __init__(self):
        self.handleMigration = Migrate()
        self.handleQuery = Query()
