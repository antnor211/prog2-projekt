from hashlib import new
import sqlite3

class Migrate:
    def __init__(self, path_database, path_sql_file):
        self.path_database = path_database
        self.con = sqlite3.connect(self.path_database)
        self.cur = self.con.cursor()
        self.path_sql_file = path_sql_file
        self.sql_file = None
        self.sql_data = None
        self.sql_query = ""
    
    def _open_sql(self): 
        self.sql_file = open(self.path_sql_file, "r")
        self.sql_data = self.sql_file.readlines()
        self.sql_file.close()
    
    def migrate_data(self):
        self._open_sql()
        for line in self.sql_data:
            new_line = line.replace("\n", "")
            if new_line == "":
                continue
            self.sql_query += new_line
            if self.sql_query.endswith(";"):
                exec_sql = self.sql_query.replace("    ", "")
                print(exec_sql)
                self.cur.execute(exec_sql)
                self.sql_query = ""
                print("END of quary line")
            else:
                continue
        self.con.commit()
        self.con.close()



migrate = Migrate("database.db", "migrate.sql")
migrate.migrate_data()