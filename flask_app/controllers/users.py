from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Number of pages shown: 2 pages
#Register/Login Page
#Dashboard - page once a user is logged in

#NUMBER of routes used: 3
#register user (register form)
#login user (user form)
#logout (dashboard page)



#Login/Register PAGE
@app.route('/')
def index():
    return render_template('index.html')


#GO MAKE index.html page - DONE


#REGISTER (POST)
@app.route('/register', methods = ["POST"])
def register():
    if not User.is_valid_reg(request.form):
        return redirect("/")
#use the save method now, but need to create a data object to hash the password
#now insert bcrypt function in front of the requst.form  for password to hash the password 
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.create(data)
    session['user_id'] = id
    return redirect('/dashboard')



#LOGIN(POST)
@app.route('/login', methods = ["POST"])
def login():
#check to see if email is in the DB
    user = User.get_by_email(request.form)
#is email address is not registerd 
    if not user:
        flash("Your email is not recognized.  Go sign up.", "login")
        return redirect('/')
#if wrong password
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect Password", "login")
        return redirect('/')

#is user makes it this far...it means their email is in the DB and password matches the DB
    session['user_id'] = user.id
    return redirect('/dashboard')


#go create dashboard.html file DONE



#DASHBOARD PAGE
@app.route('/dashboard')
def dashboard():
#always Check RIGHT AWAY if user is in session - extra secure
    if 'user_id' not in session:
        return redirect('/logout')
    
#query the DB for user information
    data = {
        "id" : session['user_id']
    }
    return render_template("dashboard.html", user = User.get_one(data))



#LOGOUT(POST)
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")