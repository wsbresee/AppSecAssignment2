from flask import Flask, render_template, request
from subprocess import check_output

INPUTTEXT_ADDR = 'input.txt'
DICTIONARY_ADDR = 'wordlist.txt'

class User:
    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone

users = []

def is_user(the_user):
    for a_user in users:
        if a_user.username == the_user.username:
            return a_user

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"
    
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    error = None
    textout = None
    if (request.method == 'POST'):
        inputtext = request.form['inputtext']
        inputtext_file = open(INPUTTEXT_ADDR, 'w')
        inputtext_file.write(inputtext)
        inputtext_file.close()
        textout=inputtext
        misspelled = check_output(['./a.out', INPUTTEXT_ADDR, DICTIONARY_ADDR]).decode('utf-8')
        misspelled = misspelled.replace('\n', ',').strip(',')
    return render_template('spell_check.html', textout=textout, misspelled=misspelled)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        if not username:
            error = 'invalid username'
        elif not password:
            error = 'invalid password'
        elif not phone:
            error = 'invalid phone'
        else:
            user = User(username, password, phone)
            maybe_the_user = is_user(user)
            if not maybe_the_user:
                error = 'Incorrect'
            elif (maybe_the_user.password != user.password):
                error = 'Incorrect'
            elif (maybe_the_user.phone != user.phone):
                error = 'Two-factor failure'
            else:
                error = 'success'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        if not username:
            error = 'invalid username'
        elif not password:
            error = 'invalid password'
        elif not phone:
            error = 'invalid phone'
        else:
            user = User(username, password, phone)
            if not is_user(user):
                users.append(user)
                error = 'success'
            else:
                error = 'failure'
    return render_template('register.html', error=error)

if (__name__ == '__main__'):
    app.run(debug=True)
