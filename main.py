from server.database.migrate import Migrate

mig = Migrate("server/database/database.db")

mig.migrate_data()