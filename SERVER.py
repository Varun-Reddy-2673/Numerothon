import datetime
import email.message
import math
import mysql.connector
import random
import re
import smtplib
import time

from flask import Flask, jsonify, request, send_from_directory

APP = Flask (__name__, static_url_path = '')
Stamp = 1601510400

@APP.route ('/FRONT_END/ACTIVATE/<Code>', methods = ['GET'])

def ACTIVATE (Code):

    Account = SQL_1 ('SELECT USERNAME, PASSWORD FROM ACCOUNTS WHERE VERIFICATION = \'' + Code + '\'')

    if len (Account) > 0:

        SQL_2 ('UPDATE ACCOUNTS SET VERIFICATION = \'COMPLETE\' WHERE VERIFICATION = \'' + Code + '\'')

        return jsonify ({'Status': True, 'Username': Account [0] [0], 'Password': Account [0] [1]})

    else:

        return jsonify ({'Status': False})

    return jsonify ({'Status': not Check (request.headers ['Authorisation'])})

@APP.route ('/FRONT_END/REFRESH', methods = ['GET'])

def REFRESH ():

    return jsonify ({'Status': not Check (request.headers ['Authorisation'])})

@APP.route ('/FRONT_END/SI_GET_ACCOUNT_INFO/<Username>/<Password>', methods = ['GET'])

def SI_GET_ACCOUNT_INFO (Username, Password):

    Account_Info_1 = SQL_1 ('SELECT ID, USERNAME, FIRST_NAME, LAST_NAME, MOBILE_NUMBER FROM ACCOUNTS WHERE USERNAME = \'' + Username + '\' AND VERIFICATION = \'COMPLETE\'')

    if (len (Account_Info_1) == 0):

        return jsonify ({'Information': '', 'Message': 'This account does not exist.'})

    else:

        Account_Info_2 = SQL_1 ('SELECT ID, USERNAME, FIRST_NAME, LAST_NAME, MOBILE_NUMBER FROM ACCOUNTS WHERE USERNAME = \'' + Username + '\' AND PASSWORD = \'' + Password + '\' AND VERIFICATION = \'COMPLETE\'')

        if (len (Account_Info_2) == 0):

            return jsonify ({'Information': '', 'Message': 'The password is incorrect.'})

        else:

            Information = Account_Info_2 [0]
            Code = Session ()

            return jsonify ({'Information': str (Information [0]) + ' | ' + Information [1] + ' | ' + Information [2] + ' | ' + Information [3] + ' | ' + Information [4] + ' | ' + Code, 'Message': ''})

@APP.route ('/FRONT_END/SU_POST_CREATE_ACCOUNT', methods = ['POST'])

def SU_POST_CREATE_ACCOUNT ():

    JSON = request.json
    Username = JSON ['E_Mail']
    Password_1 = JSON ['Password_1']
    Password_2 = JSON ['Password_2']
    First_Name = JSON ['First_Name']
    Last_Name = JSON ['Last_Name']
    Mobile_Number = JSON ['Mobile_Number']

    if (len (SQL_1 ('SELECT ID FROM ACCOUNTS WHERE USERNAME = \'' + Username + '\' AND VERIFICATION = \'COMPLETE\'')) != 0):

        return jsonify ({'Type': 'negative', 'Message': 'An account with this e-mail address already exists.'})

    if (re.search ('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', Username) == None):

        return jsonify ({'Type': 'negative', 'Message': 'Please enter a valid e-mail adress.'})

    elif (Password_1 != Password_2):

        return jsonify ({'Type': 'negative', 'Message': 'Please re-enter the password as they are not matching.'})

    elif (First_Name.isalpha () == False) or (Last_Name.isalpha () == False):

        return jsonify ({'Type': 'negative', 'Message': 'Your name can only contain letters.'})

    elif (Mobile_Number.isdigit () == False) or (len (Mobile_Number) != 10):

        return jsonify ({'Type': 'negative', 'Message': 'Mobile numbers must be 10 digits long and can only contain numerical digits.'})

    else:

        SQL_2 ('INSERT INTO ACCOUNTS SET USERNAME = \'' + Username + '\', PASSWORD = \'' + Password_1 + '\', FIRST_NAME = \'' + First_Name + '\', LAST_NAME = \'' + Last_Name + '\', MOBILE_NUMBER = \'' + Mobile_Number + '\'')

        return jsonify ({'Type': 'positive', 'Message': 'Your account has been made! We have sent an e-mail to \'' + Username + '\' for verification.'})

@APP.route ('/FRONT_END/SU_POST_VERIFY', methods = ['POST'])

def SU_POST_VERIFY ():

    Username = request.json ['E_Mail']
    Alphanum = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Check = True

    while Check:

        Code = ''

        for I in range (0, 10):

            Code += Alphanum [int (random.random () * len (Alphanum))]

        Epoch = str (int (time.time ()) - Stamp)
        Existing = SQL_1 ('SELECT ID FROM ACCOUNTS WHERE VERIFICATION = \'' + Code + '\'')

        if len (Existing) == 0:

            Check = False

    SQL_2 ('UPDATE ACCOUNTS SET VERIFICATION = \'' + Code + '\' WHERE USERNAME = \'' + Username + '\'')
    Content = '''

    <html>
        <body>
            <table style = 'margin: auto'>
                <tr>
                    <th style = 'background-color: #0d2e7a; color: #ffffff; font-size: 25px'><h1>Numerothon</h1></th>
                </tr>
                <tr>
                    <th style = 'background-color: #2c83ab; color: #ffffff; font-size: 20px'><h2>Verification</h2></th>
                </tr>
                <tr style = 'background-color: #c4edff; color: #0d2e7a; font-size: 20px'>
                    <p>An account has been made on our website with this e-mail account.</p>
                    <p>In order to sign in to your new account, <a href = 'http://0.0.0.0:4000/FRONT_END/VERIFY.html?Code=''' + Code + ''''>click here</a>.</p>
                <tr>
            </table>
            </div>
        </body>
    </html>

    '''

    Mail ('Verification', Content, Username)

    return jsonify ({'Status': True})

@APP.route ('/FRONT_END/NT_GET_CHANGE_CHAPTER/<int:Chapter_1>/<int:Chapter_2>/<int:Grade_1>/<Grade_2>', methods = ['GET'])

def NT_GET_CHANGE_CHAPTER (Chapter_1, Chapter_2, Grade_1, Grade_2):

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Chapters = SQL_1 ('SELECT ID, CHAPTER FROM CHAPTERS WHERE GRADE = ' + str (Grade_1))
        Criteria = [[Grade_1, Chapter_1], [Grade_2, Chapters [Chapter_2 - 1] [1]]]

        return jsonify ({'Status': True, 'Criteria': Criteria})

@APP.route ('/FRONT_END/NT_GET_CHANGE_GRADE/<int:Grade>', methods = ['GET'])

def NT_GET_CHANGE_GRADE (Grade):

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Grades = SQL_1 ('SELECT ID, GRADE FROM GRADES')
        Criteria = [[Grade, 0], [Grades [Grade - 1] [1], 'NOT SELECTED']]
        Chapters = SQL_1 ('SELECT ID, CHAPTER FROM CHAPTERS WHERE GRADE = ' + str (Grade))

        return jsonify ({'Status': True, 'Criteria': Criteria, 'Chapters': Chapters})

@APP.route ('/FRONT_END/NT_GET_GRADES', methods = ['GET'])

def NT_GET_GRADES ():

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Grades = SQL_1 ('SELECT ID, GRADE FROM GRADES')

        return jsonify ({'Status': True, 'Grades': Grades})

@APP.route ('/FRONT_END/NT_POST_CREATE_TEST', methods = ['POST'])

def NT_POST_CREATE_TEST ():

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        JSON = request.json
        Epoch = str (int (time.time ()) - Stamp)
        SQL_2 ('INSERT INTO TESTS SET ACCOUNT = ' + str (JSON ['Account']) + ', CHAPTER = ' + str (JSON ['Chapter']) + ', TIME = ' + Epoch)
        Test_ID = SQL_1 ('SELECT ID FROM TESTS WHERE ACCOUNT = ' + str (JSON ['Account']) + ' AND TIME = ' + Epoch)

        return jsonify ({'Status': True, 'ID': Test_ID [0] [0]})

@APP.route ('/FRONT_END/TE_GET_CREATE_BAR', methods = ['GET'])

def TE_GET_CREATE_BAR ():

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Correct_Array = []
        Loop_Index = 0

        while Loop_Index < 10:

            Correct_Array.append (['blank', 2])
            Loop_Index += 1

        Correct_Array [0] [0] = 'current'

        return jsonify ({'Status': True, 'Correct_Array': Correct_Array})

@APP.route ('/FRONT_END/TE_POST_NEW_QUESTION', methods = ['POST'])

def TE_POST_NEW_QUESTION ():

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        JSON = request.json
        Templates = SQL_1 ('SELECT QUESTION, FRAME_1, ANSWER, FRAME_2, CHOICE, FRAME_3, VAR_1, VAR_2, VAR_3, ID FROM TEMPLATES WHERE CHAPTER = ' + JSON ['Chapter'])
        Template = Templates [int (len (Templates) * random.random ())]
        Available = ''.join (sorted (set (list (Template [6]))))
        Genres = SQL_1 ('SELECT ID FROM GENRES WHERE AVAILABLE = \'' + Available + '\'')
        Subject = str (Genres [int (random.random () * len (Genres))] [0])
        Nouns = []

        for I in Available:

            Nouns.append (SQL_1 ('SELECT VALUE FROM NOUNS WHERE TYPE = ' + I + ' AND GENRE = ' + Subject))

        Output = Question (Template, Available, Nouns)
        SQL_2 ('INSERT INTO ATTEMPTS SET CHAPTER = ' + JSON ['Chapter'] + ', TEMPLATE = ' + Output [3] + ', ACCOUNT = ' + JSON ['Account'] + ', TEST = ' + JSON ['Test'] + ', QUESTION = \'' + Output [0] + '\', ANSWER = \'' + Output [1] + '\'')
        ID = SQL_1 ('SELECT ID FROM ATTEMPTS WHERE TEST = ' + JSON ['Test'])

        return jsonify ({'Status': True, 'Question': Output [0], 'Options': ' | '.join (Output [2]), 'ID': str (ID [- 1] [0])})

@APP.route ('/FRONT_END/TE_POST_SUBMIT_ANSWER', methods = ['POST'])

def TE_POST_SUBMIT_ANSWER ():

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        JSON = request.json
        Info = SQL_1 ('SELECT ANSWER FROM ATTEMPTS WHERE ID = ' + JSON ['ID'])

        if JSON ['Attempt'] == Info [0] [0]:

            Correct = '1'

        else:

            Correct = '0'

        SQL_2 ('UPDATE ATTEMPTS SET ATTEMPT = ' + JSON ['Attempt'] + ', CORRECT = ' + Correct + ', TIME = ' + str (JSON ['Time']) + ' WHERE ID = ' + JSON ['ID'])

        return jsonify ({'Status': True, 'Correct': int (Correct)})

@APP.route ('/FRONT_END/RE_GET_REPORT/<Test>', methods = ['GET'])

def RE_GET_REPORT (Test):

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Initial_Report = SQL_1 ('SELECT QUESTION, ANSWER, ATTEMPT, CORRECT, TIME, TEMPLATE FROM ATTEMPTS WHERE TEST = ' + Test + ' AND ATTEMPT IS NOT NULL')
        Final_Report = []

        for Initial_Item in Initial_Report:

            Final_Item = list (Initial_Item [0:3])

            if (Initial_Item [3] == 1):

                Final_Item.append ('positive')

            else:

                Final_Item.append ('negative')

            Final_Item.append (str (Initial_Item [4] / 1000) + ' s')
            Percentage = SQL_1 ('SELECT AVG (CORRECT) FROM ATTEMPTS WHERE TEMPLATE = ' + str (Initial_Item [5]))
            Final_Item.append (str (int (Percentage [0] [0] * 100)) + ' %')
            Final_Report.append (Final_Item)

        Accuracy = SQL_1 ('SELECT AVG (CORRECT) FROM ATTEMPTS WHERE TEST = ' + Test)

        return jsonify ({'Status': True, 'Report': Final_Report, 'Accuracy': str (int (Accuracy [0] [0] * 100)) + ' %'})

@APP.route ('/FRONT_END/RE_GET_TESTS/<Account>', methods = ['GET'])

def RE_GET_TESTS (Account):

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Initial_Tests = SQL_1 ('SELECT ID, CHAPTER, TIME FROM TESTS WHERE ACCOUNT = ' + Account + ' ORDER BY TIME DESC LIMIT 6')
        Final_Tests = []

        for Loop_Index, Test in enumerate (Initial_Tests):

            Chapter = SQL_1 ('SELECT CHAPTER FROM CHAPTERS WHERE ID = ' + str (Test[1]))
            Timestamp = datetime.datetime.fromtimestamp (Test [2] + Stamp)
            Final_Tests.append ([Test [0], Chapter [0] [0], Timestamp.strftime ('%H:%M, %d | %m | %Y')])

        return jsonify ({'Status': True, 'Tests': Final_Tests})

@APP.route ('/FRONT_END/AN_GET_TESTS/<Account>', methods = ['GET'])

def AN_GET_TESTS (Account):

    if Check (request.headers ['Authorisation']):

        return jsonify ({'Status': False})

    else:

        Tests = SQL_1 ('SELECT ID, CHAPTER, TIME FROM TESTS WHERE ACCOUNT = ' + Account + ' ORDER BY TIME DESC LIMIT 20')
        Final = []

        for Test in Tests:

            Chapter = SQL_1 ('SELECT CHAPTER FROM CHAPTERS WHERE ID = ' + str (Test [1]))
            Average = SQL_1 ('SELECT AVG (CORRECT) FROM ATTEMPTS WHERE TEST = ' + str (Test [0]))
            Time = datetime.datetime.fromtimestamp (Test [2] + Stamp)
            Final.append ([Test [0], Chapter [0] [0], int (Average [0] [0] * 100), Time.strftime ('%H:%M'), Time.strftime ('%d | %m | %Y')])

        return jsonify ({'Status': True, 'Tests': Final})

@APP.route ('/FRONT_END/<path:path>')

def Connector (path):

    return send_from_directory ('FRONT_END', path)

def Check (Code):

    Epoch = str (int (time.time ()) - Stamp)
    Sessions = SQL_1 ('SELECT ID FROM SESSIONS WHERE CODE = \'' + Code + '\' AND LAST_ACTIVE > ' + str (int (Epoch) - 600))

    if len (Sessions) == 0:

        return True

    else:

        SQL_2 ('UPDATE SESSIONS SET LAST_ACTIVE = ' + Epoch + ' WHERE ID = ' + str (Sessions [0] [0]))

        return False

def Question (Template, Available, Nouns):

    Alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Variables = [{}, {}, {}]
    Chosen = []

    for H, I in enumerate (list (Template [6])):

        Check = True

        while Check:

            Index = Available.find (I)
            New = Nouns [Index] [int (len (Nouns [Index]) * random.random ())] [0]
            Check = New in Chosen

        Variables [0] [Alpha [H]] = New
        Chosen.append (New)

    for H, I in enumerate (Template [7].split ('|')):

        Range = I.split (':')
        New = int ((int (Range [1]) - int (Range [0])) * random.random ()) + int (Range [0])
        Variables [1] [Alpha [H]] = New

    Question = Replace (Template [0].split ('|'), list (Template [1]), Variables)
    Answer = Replace (Template [2].split ('|'), list (Template [3]), Variables)
    Options = []

    for Z in range (0, 3):

        Check = True

        while Check:

            for H, I in enumerate (Template [8].split ('|')):

                Range = I.split (':')
                New = int ((int (Range [1]) - int (Range [0])) * random.random ()) + int (Range [0])
                Variables [2] [Alpha [H]] = New

            New = Replace (Template [4].split ('|'), list (Template [5]), Variables)
            Check = New in Options or New == Answer

        Options.append (New)

    Options.insert (int (random.random () * 4), Answer)

    return [Question, Answer, Options, str (Template [9])]

def Replace (Proper, Frame, Variables):

    Final = ''

    for H, I in enumerate (Frame):

        if I == '0':

            Final += Proper [H]

        elif I == '1':

            for J in list (Variables [0]):

                Proper [H] = Proper [H].replace (J, '\'' + Variables [0] [J] + '\'')

            Final += eval (Proper [H])

        elif I == '2':

            for J in list (Variables [1]):

                Proper [H] = Proper [H].replace (J + '!', str (Variables [1] [J]))

            for J in list (Variables [2]):

                Proper [H] = Proper [H].replace (J + '?', str (Variables [2] [J]))

            Final += str (eval (Proper [H]))

    return Final

def Session ():

    Alphanum = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Check = True

    while Check:

        Code = ''

        for I in range (0, 10):

            Code += Alphanum [int (random.random () * len (Alphanum))]

        Epoch = str (int (time.time ()) - Stamp)
        Existing = SQL_1 ('SELECT ID FROM SESSIONS WHERE CODE = \'' + Code + '\' AND LAST_ACTIVE > ' + str (int (Epoch) - 600))

        if len (Existing) == 0:

            Check = False

    SQL_2 ('INSERT INTO SESSIONS SET CODE = \'' + Code + '\', LAST_ACTIVE = ' + Epoch)

    return Code

def SQL_1 (Command):

    Database = mysql.connector.connect (host = 'localhost', user = 'root', passwd = 'Lemon?2022', database = 'INDUCTION')
    Cursor = Database.cursor ()
    Cursor.execute (Command)

    return Cursor.fetchall ()

def SQL_2 (Command):

    Database = mysql.connector.connect (host = 'localhost', user = 'root', passwd = 'Lemon?2022', database = 'INDUCTION')
    Cursor = Database.cursor ()
    Cursor.execute (Command)
    Database.commit ()

def Mail (Subject, Content, Target):

    Message = email.message.Message()
    Message ['Subject'] = Subject
    Message ['From'] = 'numerothon.services@gmail.com'
    Message ['To'] = Target
    Message.add_header ('Content-Type', 'text/html')
    Message.set_payload (Content)
    Server = smtplib.SMTP ('smtp.gmail.com:587')
    Server.starttls ()
    Server.login (Message ['From'], 'wcdbacjyohckiraq')
    Server.sendmail (Message ['From'], [Message ['To']], Message.as_string ())

if (__name__ == '__main__'):

    APP.run (debug = True, host = '0.0.0.0', port = 4000)