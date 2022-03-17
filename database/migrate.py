import sqlite3

con = sqlite3.connect("database.db")

cur = con.cursor()

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
        print(sqlite_query)
        cur.execute(sqlite_query)
        sqlite_query = ""
        print("end")
    else:
        continue


con.commit()
con.close()