from flask import Flask, render_template
from subprocess import call

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
        if a_user == the_user:
            return True
    return False

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
    if (request.method == 'POST'):
        inputtext = request.form['inputtext']
        inputtext_file = open(INPUTTEXT_ADDR, 'w')
        inputtext_file.write('inputtext')
        inputtext_file.close()
        response = call(['spell_check', INPUTTEXT_ADDR, DICTIONARY_ADDR])
#not finished, add handler for actually posting results
    return render_template('spell_check.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        if (!username):
            error = 'invalid username'
        else if (!password):
            error = 'invalid password'
        else if (!phone):
            error = 'invalid phone'
        else
            user = User(username, password, phone)
            if (!is_user(user)):
                error = 'not a registered user'
            else:
                return redirect(url_for('spell_check'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        if (!username):
            error = 'invalid username'
        else if (!password):
            error = 'invalid password'
        else if (!phone):
            error = 'invalid phone'
        else:
            users.append(User(username, password, phone))
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

if (__name__ == '__main__'):
    app.run(debug=True)
