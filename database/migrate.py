import sqlite3

sql_file = open("migrate.sql", "r")
sql_data = sql_file.readlines()
sql_file.close()

print(sql_data)

sqlite_query = ""

for line in sql_data:
    new_line = line.replace("\n", "")

    if new_line == "":
        continue
    sqlite_query += new_line
    if sqlite_query.endswith(";"):
        exec_sql = sqlite_query.replace("    ", "")
        print(exec_sql)
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(exec_sql)
        con.commit()
        con.close()
        sqlite_query = ""
        print("END")
    else:
        continue
