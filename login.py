from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from auth import authenticate

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample1'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase1'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        user=request.form['username']
        password = request.form['pass']
        auth = authenticate(user,password)
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