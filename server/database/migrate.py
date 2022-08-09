from server.database.Action import Action

import termcolor
import os


class Migrate(Action):
    def __init__(self, pathDatabase):
        Action.__init__(self, pathDatabase)
        self._pathSqlFile = "server/database/migrate.sql"
        self._sqlFile = None
        self._sqlData = None
        self._sqlQuery = ""
    
    def _openSqlFile(self): 
        self._sqlFile = open(self._pathSqlFile, "r")
        self._sqlData = self._sqlFile.readlines()
        self._sqlFile.close()
    
    def migrateData(self):
        self. _openSqlFile()
        for line in self._sqlData:
            new_line = line.replace("\n", "")
            if new_line == "":
                continue
            self._sqlQuery += new_line
            if self._sqlQuery.endswith(";"):
                execSql = self._sqlQuery.replace("    ", "")
                print(execSql)
                self._cur.execute(execSql)
                self._sqlQuery = ""
                print("END of quary line")
            else:
                continue
        self._con.commit()
        
        os.system("cls" if os.name == "nt" else "clear")
        reset_message = """

██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗        ██╗    ██╗ █████╗ ███████╗        ██████╗ ███████╗███████╗███████╗████████╗██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝        ██║    ██║██╔══██╗██╔════╝        ██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝██║
██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗          ██║ █╗ ██║███████║███████╗        ██████╔╝█████╗  ███████╗█████╗     ██║   ██║
██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝          ██║███╗██║██╔══██║╚════██║        ██╔══██╗██╔══╝  ╚════██║██╔══╝     ██║   ╚═╝
██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗        ╚███╔███╔╝██║  ██║███████║        ██║  ██║███████╗███████║███████╗   ██║   ██╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝         ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝        ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝
                                                                                                                                                       

        """
        print(termcolor.colored(reset_message, "red"))
