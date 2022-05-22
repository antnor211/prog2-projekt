import sys


import sys
import os
sys.path.append(os.getcwd())

from server.database.migrate import Migrate
from server.database.Action import Action

mig = Migrate("server/database/database.db")

mig.migrateData()
