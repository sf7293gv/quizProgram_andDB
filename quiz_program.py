import sqlite3
import time
from sqlite3.dbapi2 import connect


db = 'quizDatabase.db'

""" This method will get all the topics/categories available in the table """
def get_quiz_topics():
    topics_list = []
    with sqlite3.connect(db) as conn:
        try:
            result = conn.execute('SELECT category FROM questionTable')
            for r in result:
                if topics_list.__contains__(r[0]) == False:
                    topics_list.append(r[0])
        except sqlite3.Error:
            print('Error fetching table')
        
    conn.close()
    return topics_list


""" This method will list the topics available to the user and get his/her topic choice"""
def topic_user_choice(topics_list):

    while (True):
        print('Choose the number of one of these topics, to be quizzed on: ')

        for i in range(0, len(topics_list)):
            print(f'{i+1}- {topics_list[i]}')
        
        choice = int(input())
        if choice <= len(topics_list) and choice > 0:
            break
    choice = choice - 1
    categoryChoice = topics_list[choice]
    return categoryChoice

""" This method will get the question and answers from the db and store them in a dictionary"""
def get_questions_answers(topic):
    qandaDict = {}
    counter = 0
    with sqlite3.connect(db) as conn:
        try:
            query = conn.execute('select * from questionTable where category = ?', (topic,))
            for r in query:
                question = r[1]
                category = r[6]
                difficulty = r[7]
                question_points = r[8]
                question_id = r[0]
                qInfo_list = (question, category, difficulty, question_points, question_id)
                answerList = (r[2], r[3], r[4], r[5])
                qandaDict[qInfo_list] = answerList
                counter = counter + 1
        except sqlite3.Error:
            print('Error fetching data from table')
    conn.close()
    return (qandaDict, counter)

""" This method will show the user the amount of questions for a topic, 
will ask how many questions user wants to answer and list questions/info, 
will list the answer list for each question and will store/compare the user answer """
def quiz_user(qandaDict, amountQuestions): 
    while (True):
        nq = int(input(f'Topic has {amountQuestions} questions. How many do you want to answer? '))
        if nq > 0 and nq <= amountQuestions:
            break

    c = 0
    answers = {}
    for item in qandaDict.items():
        if c < nq:
            question = item[0][0]
            category = item[0][1]
            difficulty = item[0][2]
            q_points = item[0][3]
            q_id = item[0][4]
            print(f'Question: {question}, category: {category}, difficulty: {difficulty}, points available: {q_points}, question id: {q_id}')
            print('choose one of these answers for the question: ')
            for i in range (0, len(item[1])):
                print(f'{i+1}- {item[1][i]}')
            while (True):
                user_input = int(input('Choose the number of the answer: '))
                if user_input > 0 and user_input <= len(item[1]):                    
                    break
            
            user_answer = item[1][user_input - 1]
            correct_answer = item[1][0]
            q_data = (question, category, difficulty, q_points, q_id)
            answers[q_data] = (user_answer,correct_answer)
            
            c = c + 1
        else:
            break
    return answers


""" This method will be passed a dictionary that contains 
    (questions, user answers, correct answers) and will compare between the answers """
def compare_answers(answers_dict):
    for key, value in answers_dict.items():
        question = key
        user_answer = value[0]
        correct_answer = value[1]
        print('key val pair:')
        print(key, value)
        
        print(f'For the question: {question} User answer: {user_answer}, Correct answer: {correct_answer}')
        if (user_answer == correct_answer):
            print('Correct!!')
        else:
            print(f'Correct answer: {correct_answer}')


# insert INTO quiz_results (userID, qID, timeStarted, timeEnded, question, answer, correct, questionPoints, pointsEarned)VALUES (
# 	"one", 1, 10, 11, 1, 2, 1, 20, 15
# );

""" This method will be passed two dictionaries, first one contains questions and user answers,
    second contains more data for each question 
    and will insert new rows to the quiz_results table in the database """
def add_info_quiz_results_table(user_answers_dict):
    user_name = get_user_id()
    with sqlite3.connect(db) as conn:
        try:
            query = 'insert INTO quiz_results (userID, qID, timeStarted, timeEnded, question, answer, correct, questionPoints, pointsEarned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'        
            for item in user_answers_dict.items():
                qID = item[0][4]
                timestarted = time.asctime()
                timeended = time.asctime()
                q = item[0][0]
                uA = item[1][0]
                qA = item[1][1]
                correct = 2
                questionPoints = item[0][3]
                pointsEarned = 150
                if uA == qA:
                    correct = 1
                    pointsEarned = questionPoints
                else:
                    correct = 0
                    pointsEarned = 0
                
                list = (user_name, qID, timestarted, timeended, q, uA, correct, questionPoints, pointsEarned)
                print(list)
                conn.execute(query, list)
                print(item)                
        except sqlite3.Error:
            print('Error inserting data to table')

""" This method will ask the user for their user name and return it """
def get_user_id():
    userID = ""
    while (True):
        userID = input("Enter user name: ")
        if (userID != ""):
            break
    return userID
        

list = get_quiz_topics()
user_topic_choice = topic_user_choice(list)
res = get_questions_answers(user_topic_choice)
question_dictionary = res[0]
questions_amount = res[1]
user_answers_dict = quiz_user(question_dictionary, questions_amount)
compare_answers(user_answers_dict)
add_info_quiz_results_table(user_answers_dict)
