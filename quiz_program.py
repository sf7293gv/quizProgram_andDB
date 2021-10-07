import sqlite3
from sqlite3.dbapi2 import connect

# db = sqlite3.connect('quizDatabase.db')

# cur = db.cursor()

# result = cur.execute('SELECT category FROM questionTable')

db = 'quizDatabase.db'

""" This method will get all the topics/categories avaliable in the table """
def get_quiz_topics():
    topics_list = []
    with sqlite3.connect(db) as conn:
        result = conn.execute('SELECT category FROM questionTable')
        for r in result:
            if topics_list.__contains__(r[0]) == False:
                topics_list.append(r[0])
    conn.close()
    return topics_list


""" This method will list the topics avaliable to the user and get his/her topic choice"""
def topic_user_choice(topics_list):
    print('Choose the number of one of these topics, to be quizzed on: ')

    for i in range(0, len(topics_list)):
        print(f'{i+1}- {topics_list[i]}')

    choice = int(input())
    choice = choice - 1
    categoryChoice = topics_list[choice]
    return categoryChoice

""" This method will get the question and answers from the db and store them in a dictionary"""
def get_questions_answers(topic):
    qandaDict = {}
    with sqlite3.connect(db) as conn:
        query = conn.execute('select * from questionTable where category = ?', (topic,))
        counter = 0
        for r in query:
            question = (r[1])
            answerList = (r[2], r[3], r[4], r[5])
            qandaDict[question] = answerList
            counter = counter + 1
    conn.close()
    return qandaDict


list = get_quiz_topics()
user_topic_choice = topic_user_choice(list)
qNaDictionary = get_questions_answers(user_topic_choice)


# topics_list.append(firstRow[0])




    
    




# query = db.execute(f'select * from questionTable where category = "{categoryChoice}"')




# nq = int(input(f'{categoryChoice} has {counter} questions. How many do you want to answer? '))

# c = 0

# for item in qandaDict.items():
#     if c < nq:
#         print(f'Question: {item[0]}')
#         print('choose one of these answers for the question: ')
#         for i in range (0, len(item[1])):
#             print(f'{i+1}- {item[1][i]}')
#         user_input = int(input('Choose the number of the answer: '))
#         user_answer = item[1][user_input - 1]
#         correct_answer = item[1][0]
#         print(f'Your answer is : {user_answer}')
#         if (user_answer == correct_answer):
#             print('Correct!!')
#         else:
#             print(f'Correct answer: {correct_answer}')

#         # print(item[1][0])
#         c = c + 1
#     else:
#         break