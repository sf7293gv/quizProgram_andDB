import sqlite3
from sqlite3.dbapi2 import connect

db = 'quizDatabase.db'

conn = sqlite3.connect(db)

result = conn.execute('SELECT * FROM questionTable')
qandaDict = {}
for r in result:
    question = r[1]
    category = r[6]
    difficulty = r[7]
    question_points = r[8]
    qInfo_list = (question, category, difficulty, question_points)
    answerList = (r[2], r[3], r[4], r[5])
    qandaDict[qInfo_list] = answerList
    # counter = counter + 1

for item in qandaDict.items():
    print(item)
