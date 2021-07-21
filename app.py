# List Bible info, Catechism Info, and church location data (maybe).
# Send daily email to your email list about a Catholic question/answer.
# Figure out why 'passwordfield' doesn't work.

# Imports
from flask import (Flask, render_template, url_for, session, request, flash, redirect)
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
import sqlite3 as sql
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool)


# Prep work: Secret Key, classes, yada yada yada
app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkeythatonlyishouldknow'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///peritus_database.db"
Bootstrap(app)
db = SQLAlchemy(app)

# User class for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))

# Login Class
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 4, max = 15)])
    password = PasswordField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])
    remember = BooleanField('Remember Me')

# Registration Class
class RegisterForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email(message = 'Invalid Email'), Length(max = 50)])
    username = StringField('Username', validators = [InputRequired(), Length(min = 4, max = 15)])
    password = StringField('Password', validators = [InputRequired(), Length(min = 8, max = 80)])



# Routing.
# Signup Page
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created.</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form = form)

# Login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form = form)


# Home Page
@app.route('/')
@app.route('/home') # another option for same page
def app_title():
    return render_template('index.html')

# Profile Page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Bible page?
@app.route('/bible')
def bible():
    return render_template('bible.html')

# About Page
@app.route('/about')
def about_page():
    return render_template('about_page.html')

# Parish Page
@app.route('/parish')
def parish():
    return render_template('parish.html', pitt_dio = pitt_dio)

# Catechesis Pages.
# Page 1: Confession
@app.route('/confession')
def confession_page():
    return render_template('catechesis_one_confession.html')





# Email authentication page
@app.route('/email', methods = ['GET', 'POST'])
def email_signup():
    if request.method == 'GET':
        return '<form action = "/" method = "POST"><input name = "email"<input type = "submit"></form>'
    return 'The email you entered is {}'.format(request.form['email'])





# Database Stuff.
# Create 'user' table
db.create_all()

# Ending.
if __name__ == "__main__":
    app.run(debug = True)
