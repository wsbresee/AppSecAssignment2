from flask import Flask, render_template, request, make_response, session
from flask_wtf.csrf import CSRFProtect
from subprocess import check_output
import os

INPUTTEXT_ADDR = 'input.txt'
DICTIONARY_ADDR = 'wordlist.txt'
SECRET_KEY = os.urandom(32)

class User:
    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone
        self.is_logged_in = False

users = []

def get_user(the_user):
    for a_user in users:
        if a_user.username == the_user.username:
            return a_user

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
app.config.update(PERMANENT_SESSION_LIFETIME=600)
app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return login();

@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    textout = None
    misspelled = None
    if (request.method == 'POST'):
        if 'username' in session:
            username = session['username']
            password = session['password']
            phone = session['phone']
            user = get_user(User(username, password, phone))
        else:
            user = None
        if user and user.password == password and user.phone == phone and user.is_logged_in:
            inputtext = request.form['inputtext']
            inputtext_file = open(INPUTTEXT_ADDR, 'w')
            inputtext_file.write(inputtext)
            inputtext_file.close()
            textout=inputtext
            misspelled = check_output(['./a.out', INPUTTEXT_ADDR, DICTIONARY_ADDR]).decode('utf-8')
            misspelled = misspelled.replace('\n', ',').strip(',')
        else:
            textout = "Invalid user. Please log in."
    response = make_response(render_template('spell_check.html', textout=textout, misspelled=misspelled))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("log in function")
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
            maybe_the_user = get_user(user)
            if not maybe_the_user:
                error = 'Incorrect'
            elif (maybe_the_user.password != user.password):
                error = 'Incorrect'
            elif (maybe_the_user.phone != user.phone):
                error = 'Two-factor failure'
            else:
                error = 'success'
                session['username'] = username
                session['password'] = password
                session['phone'] = phone
                maybe_the_user.is_logged_in = True
    response = make_response(render_template('login.html', error=error))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

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
            if not get_user(user):
                users.append(user)
                error = 'success'
            else:
                error = 'failure'
    response = make_response(render_template('register.html', error=error))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if (__name__ == '__main__'):
    app.run(debug=True)
