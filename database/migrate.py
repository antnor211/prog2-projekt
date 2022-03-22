import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

sql_file = open("migrate.sql", "r")
sql_data = sql_file.readlines()
sql_file.close()


sqlite_query = ""

for line in sql_data:
    new_line = line.replace("\n", "")

    if new_line == "":
        continue
    sqlite_query += new_line
    if sqlite_query.endswith(";"):
        exec_sql = sqlite_query.replace("    ", "")
        print(exec_sql)
        cur.execute(exec_sql)
        sqlite_query = ""
        print("END")
    else:
        continue


con.commit()
con.close()