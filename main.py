from server.database.migrate import Migrate
from server.database.Action import Action

mig = Migrate("server/database/database.db")

mig.migrate_data()
