#  makes render template work using jinja2 
import os
from flask import Flask, flash, session, render_template, redirect,  request, url_for,request
from flask_wtf.csrf import CSRFProtect 
from .forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import bcrypt
from flask_login import user_loaded_from_header, LoginManager



# take code and put it in init.py
app = Flask(__name__)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
# Setup CSRF secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)
# setup databases
app.config['SQLALCHEMY_DATABASE_URI'] ='User' 
SQLAlchemy(app)
# Make Login user work 
login_manager = LoginManager() 
login_manager.init_app(app)
# confused what this does.
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



#todo turn into a database why is there no post number like 1st post ever posted in general etc?
posts = {   
    "username": "author",
    "author": "Bobby Bobson",
    "Title": "Hello World",
    "Content": "This is a post content 1",
    "date_posted": "March 17 2021" 
}




@app.route("/about")
def about():
    return render_template('about.html')


   

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit():?
    if request.method == 'POST' and form.validate():
        # get data from wtf forms 
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_db = user_db(username=username, email=email, hashed_password=hashed_password)
        db.session.add(user_db)
        # session commit what does this do
        db.session.commit()
        # todo make it so user can't input no username or password in flask important or is what if request.method == 'POST' and form.validate(): does that  etc  
        # login user Should I use next or login
        login_user(user_db)                                         
        flash('You have registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html',title='register', form=form)

@app.route("/login",methods = ['POST', 'GET'])
def login():
    form = LoginForm()   
    if request.method == 'POST' and form.validate():
        # Querying Records
        # check if username or password inputted in login forms matches the database
        username = form.username.data
        # do I need .first()?
        db_username= User.query.filter_by(username=username).first()

        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # login user
        db_hashed_password = User.query.filter_by(hashed_password=hashed_password).first()
        user_db = user_db(db_username=db_username,db_hashed_password=db_hashed_password)
        login_user(user_db) 
        flash('You have logged in successfully') 

    return render_template('login.html',title='login', form=form)


# read the post
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)
@app.route("/logoff")
def logoff():
    return render_template('home.html')
# create the posts
@app.route("/post")
def post():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

#db.execute
    