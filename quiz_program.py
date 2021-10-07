import sqlite3

db = sqlite3.connect('quizDatabase.db')

cur = db.cursor()

result = cur.execute('SELECT category FROM questionTable')
# firstRow = cur.fetchone()

topics_list = []

# topics_list.append(firstRow[0])

counter = 0

for r in result:
    if topics_list.__contains__(r[0]) == False:
        topics_list.append(r[0])
    
    



print('Choose the number of one of these topics, to be quizzed on: ')

for i in range(0, len(topics_list)):
    print(f'{i+1}- {topics_list[i]}')

choice = int(input())
choice = choice - 1
categoryChoice = topics_list[choice]
print(choice)
print(categoryChoice)

query = db.execute(f'select * from questionTable where category = "{categoryChoice}"')
qandaDict = {}
counter = 0

for r in query:
    question = (r[1])
    answerList = (r[2], r[3], r[4], r[5])
    qandaDict[question] = answerList
    counter = counter + 1



nq = int(input(f'{categoryChoice} has {counter} questions. How many do you want to answer? '))

c = 0

for item in qandaDict.items():
    if c < nq:
        print(f'Question: {item[0]}')
        print('choose one of these answers for the question: ')
        for i in range (0, len(item[1])):
            print(f'{i+1}- {item[1][i]}')
        user_input = int(input('Choose the number of the answer: '))
        user_answer = item[1][user_input - 1]
        print(f'Your answer is : {user_answer}')
        # print(item[1][0])
        c = c + 1
    else:
        break