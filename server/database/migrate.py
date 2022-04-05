from server.database.Action import Action

import termcolor
import os


class Migrate(Action):
    def __init__(self, path_database, path_sql_file):
        Action.__init__(self, path_database)
        self._path_sql_file = path_sql_file
        self._sql_file = None
        self._sql_data = None
        self._sql_query = ""
    
    def _open_sql_file(self): 
        self._sql_file = open(self._path_sql_file, "r")
        self._sql_data = self._sql_file.readlines()
        self._sql_file.close()
    
    def migrate_data(self):
        self._open_sql_file()
        for line in self._sql_data:
            new_line = line.replace("\n", "")
            if new_line == "":
                continue
            self._sql_query += new_line
            if self._sql_query.endswith(";"):
                exec_sql = self._sql_query.replace("    ", "")
                print(exec_sql)
                self._cur.execute(exec_sql)
                self._sql_query = ""
                print("END of quary line")
            else:
                continue
        self._con.commit()
        self._con.close()

        os.system("cls" if os.name == "nt" else "clear")
        reset_message = """

██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗        ██╗    ██╗ █████╗ ███████╗        ██████╗ ███████╗███████╗███████╗████████╗██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝        ██║    ██║██╔══██╗██╔════╝        ██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝██║
██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗          ██║ █╗ ██║███████║███████╗        ██████╔╝█████╗  ███████╗█████╗     ██║   ██║
██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝          ██║███╗██║██╔══██║╚════██║        ██╔══██╗██╔══╝  ╚════██║██╔══╝     ██║   ╚═╝
██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗        ╚███╔███╔╝██║  ██║███████║        ██║  ██║███████╗███████║███████╗   ██║   ██╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝         ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝        ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝
                                                                                                                                                       

        """
        print(termcolor.colored(reset_message, "green"))



migrate = Migrate("database.db", "migrate.sql")
migrate.migrate_data()