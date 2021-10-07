import sqlite3
from sqlite3.dbapi2 import connect

db = 'quizDatabase.db'

conn = sqlite3.connect(db)

result = conn.execute('SELECT * FROM questionTable')

for r in result:
    print(r)