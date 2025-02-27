import sqlite3

with sqlite3.connect('database.db') as db:
    cur = db.cursor()
    cur.execute("SELECT * FROM targets")

    rows = cur.fetchall()
    for row in rows:
        print(row)

