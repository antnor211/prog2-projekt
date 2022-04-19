from server.database.migrate import Migrate

mig = Migrate("database.db")

mig.migrate_data()