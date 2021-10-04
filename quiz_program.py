import sqlite3

db = sqlite3.connect('quizDatabase.db')

cur = db.cursor()

result = cur.execute('SELECT category FROM questionTable')

for r in result:
    print(r)

