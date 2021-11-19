import sqlite3
import time
from sqlite3.dbapi2 import Error, connect

# This file has a lot going on. There's user interaction, database interaction, tracking time... 
# it should be split into separate modules, each with a particular focus 

db = 'quizDatabase.db'

def get_quiz_topics():
    """ We know it's a method. This is shorter, to the point, conveys same information. 
    Get all the topics/categories available in the table """
    topics_list = []
    with sqlite3.connect(db) as conn:
        try:
            result = conn.execute('SELECT category FROM questionTable')
            for r in result:
                # don't use __contains__ it's a method that's called when you use the in operator, or not in,
                if r[0] not in topics_list: 
                # if topics_list.__contains__(r[0]) == False:
                    topics_list.append(r[0])
        except sqlite3.Error as e:
            print(e) # or log e   All kinds of things can go wrong. You'll have no idea if you print a general error message
            # having access to the stack trace, exception info is more helpful. Same comment for other DB error handlers
            print('Error fetching table')  # is that what went wrong?
        
    conn.close()  
    return topics_list


""" This method will list the topics available to the user and get his/her topic choice"""
def topic_user_choice(topics_list):

    while (True):
        print('Choose the number of one of these topics, to be quizzed on: ')

        # or use enumerate 
        # for i, topic in enumerate(topics_list):
        #     print(f'{i+1}- {topic}')


        for i in range(0, len(topics_list)):
            print(f'{i+1}- {topics_list[i]}')
        try:
            choice = int(input())
            if choice <= len(topics_list) and choice > 0:
                break
        except ValueError:
            print('Enter a valid number.')

    choice = choice - 1   # offsetting by 1 is very error prone. Can you think of a way to avoid this? 
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
                # use the row factory so you can write 
                # question = r['question']
                # instead of remembering the indexes of the columns. 
                # code is more readable too. 

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
    will ask how many questions user wants to answer """
def amount_of_questions_to_ask(amountQuestions):
    while (True):
        try:
            # avoid abbreviations. 
            number_of_questions = int(input(f'Topic has {amountQuestions} questions. How many do you want to answer? '))
            if number_of_questions > 0 and number_of_questions <= amountQuestions:
                break
        except ValueError:
            print('Enter a valid number.')
    return number_of_questions


""" This method  and list questions/info, 
will list the answer list for each question and will store/compare the user answer """
def quiz_user(qandaDict, user_questions_amount):     
    c = 0  # what is this variable for? It needs a better name 
    answers = {}
    for item in qandaDict.items():
        if c < user_questions_amount:
            question = item[0][0]
            category = item[0][1]
            difficulty = item[0][2]
            q_points = item[0][3]
            q_id = item[0][4]

            print(f'Question: {question}, category: {category}, difficulty: {difficulty}, points available: {q_points}, question id: {q_id}')
            print('choose one of these answers for the question: ')

            for i in range (0, len(item[1])):  # enumerate is cleaner and less typing 
                print(f'{i+1}- {item[1][i]}')

            # this detail - getting a valid choice - can be delegated to a seprate function 
            while (True):
                try:
                    user_input = int(input('Choose the number of the answer: '))
                    if user_input > 0 and user_input <= len(item[1]):                    
                        break
                except ValueError:
                    print('Enter a valid number.')
            
            user_answer = item[1][user_input - 1]
            correct_answer = item[1][0]  # What's happening here? 
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
        user_answer = value[0]  # what are these indexes? 
        correct_answer = value[1]     
        print(f'For the question: {question[0]} User answer is: {user_answer}')
        if (user_answer == correct_answer):
            print('Correct!!')
        else:
            print(f'Correct answer: {correct_answer}')


""" This method will be passed two dictionaries, first one contains questions and user answers,
    second contains more data for each question 
    and will insert new rows to the quiz_results table in the database """
def add_info_quiz_results_table(user_answers_dict, user_name):    
    with sqlite3.connect(db) as conn:
        try:
            query = 'insert INTO quiz_results (userID, qID, timeStarted, timeEnded, question, answer, correct, questionPoints, pointsEarned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'        
            for item in user_answers_dict.items():
                qID = item[0][4]  # what are these indexes? 
                timestarted = time.asctime()
                timeended = time.asctime()
                q = item[0][0]    # use specific names 
                uA = item[1][0]   # and here
                qA = item[1][1]   # and here too
                correct = 2
                questionPoints = item[0][3]   # question_points - and what are these indexes?? 
                pointsEarned = 150   # be consistent with variable names casing, so points_earned 
                if uA == qA:
                    correct = 1
                    pointsEarned = questionPoints
                else:
                    correct = 0
                    pointsEarned = 0
                
                list = (user_name, qID, timestarted, timeended, q, uA, correct, questionPoints, pointsEarned)
                print(list)
                conn.execute(query, list)
                # print(item)                
        except sqlite3.Error:
            print('Error inserting data to table')
    conn.close()

""" This method will ask the user for their user name and return it """
def get_user_id():
    userID = ""
    while (True):
        userID = input("Enter user name: ")
        if (userID != ""):
            break
    return userID

""" This method will show results show below to user """
def get_quiz_results(questions_amount, correctQamount, pointsAvailable, pointsEarned):
    time_taken = quiz_end_time - quiz_start_time
    time_taken = '%.2f' % time_taken
    print(f'It took you {time_taken} seconds to finish the quiz.')
    print(f'Amount of questions you answered: {questions_amount}')
    print(f'Amount of questions answered correctly by user: {correctQamount}')
    print(f'Amount of points available: {pointsAvailable}')
    print(f'Amount of points earned: {pointsEarned}')

""" This method will get the amount of questions answerd right by the user from the table """
def amount_of_correct_answers_for_user(user_name):
    with sqlite3.connect(db) as conn:
        try:
            sql = conn.execute("SELECT count(*) as 'result' from quiz_results where correct = 1 and userID = ?", (user_name,))
            result = sql.fetchone()
            correct_answers_amount = result[0]
            return correct_answers_amount
        except sqlite3.Error:
            print('Error fetching data from table')
    conn.close()
    return

""" This method will get the points available for the questions that the user answered from table """
def amount_of_points_available(user_name):
    with sqlite3.connect(db) as conn:
        try:
            sql = conn.execute("SELECT sum(questionPoints) as 'result' from quiz_results where userID = ?", (user_name,))
            result = sql.fetchone()
            points_available = result[0]
            return points_available
        except sqlite3.Error:
            print('Error fetching data from table')
    conn.close()

""" This method will get the points earned for the questions that the user answered correctly """
def amount_of_points_earned(user_name):
    with sqlite3.connect(db) as conn:
        try:
            sql = conn.execute("SELECT sum(pointsEarned) as 'result' from quiz_results where userID = ?", (user_name,))
            result = sql.fetchone()
            points_earned = result[0]
            return points_earned
        except sqlite3.Error:
            print('Error fetching data from table')
    conn.close()


""" This method will delete all rows in the table """
def clear_quiz_results_table():
    with sqlite3.connect(db) as conn:
        try:
            sql = 'DELETE FROM quiz_results'
            conn.execute(sql)
        except sqlite3.Error:
            print('Error deleting data from table')
    conn.close()


# put this in a main function. Otherwise all this code will run when you import this file into 
# a test file
list = get_quiz_topics()
user_topic_choice = topic_user_choice(list)
res = get_questions_answers(user_topic_choice)
question_dictionary = res[0]
questions_amount = res[1]
quiz_start_time = time.time()
user_questions_amount = amount_of_questions_to_ask(questions_amount)
user_answers_dict = quiz_user(question_dictionary, user_questions_amount)
compare_answers(user_answers_dict)
quiz_end_time = time.time()
user_name = get_user_id()
add_info_quiz_results_table(user_answers_dict, user_name)
correctQamount = amount_of_correct_answers_for_user(user_name)
pointsAvailable = amount_of_points_available(user_name)
pointsEarned = amount_of_points_earned(user_name)
get_quiz_results(user_questions_amount, correctQamount, pointsAvailable, pointsEarned) 