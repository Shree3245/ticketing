from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from auth import authenticate
# to run mongodb from cmd type in "C:\Program Files\MongoDB\Server\4.04\bin\mongod.exe" 
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample1'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')

    else:
        return redirect(url_for('index'))

@app.route('/assign', methods=['POST', 'GET'])
def assign():
    if 'username' in session:
        
        ticket = request.form['ticket']
        return ticket
    return render_template('assign.html')

@app.route("/ticketConfirm")
def ticketConfirm():
    return 'x'
@app.route('/viewTicket')
def viewTicket():
    return "View"

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        user=request.form['username']
        password = request.form['pass']
        global uID
        auth,uID = authenticate(user,password)
        if auth == 'success':
            return redirect(url_for('secondAuth'))
        else:
            return "That username/password is not in the database"
        

    return render_template('register.html')



@app.route('/secondAuth', methods=['POST', 'GET'])
def secondAuth():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('secondAuth.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)