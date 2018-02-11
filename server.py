from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
import datetime
import time

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

PW_REGEX = re.compile(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$')

app = Flask(__name__)

app.secret_key = 'RegistrationFormKey'

@app.route('/')

def display_index():   
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():

    valid = True
    items = 'first'

    session['first_name'] = first_name = request.form['first_name']
    session['last_name'] = last_name = request.form['last_name']
    session['email'] = email = request.form['email']
    session['dob'] = dob = request.form['dob']

    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')

    # print dob
    # print dob < currentDate

    password = request.form['password']
    confirm_pw = request.form['confirm_pw']

    if len(session['first_name']) < 1:
        flash("First name cannot be blank!", 'red')
        valid = False
        items = 'second'
    else:
        flash("hidden", "hidden")

    if len(session['last_name']) < 1:
        flash("Last name cannot be blank!", 'red ')
        valid = False
    else:
        flash("hidden", "hidden")

    if len(session['email']) < 1:
        flash("Email cannot be blank!", 'red')
        valid = False
    elif not EMAIL_REGEX.match(session['email']):
        flash("Invalid Email Address!", 'red')
        valid = False
    else:
        flash("hidden", "hidden")
    
    if len(session['dob']) < 1:
        flash("Birth date cannot be blank!", 'red')
        valid = False
    elif dob > currentDate:
        flash("Birth date cannot be in the future!", 'red')
        valid = False
    else:
        flash("hidden", "hidden")

    if len(password) < 1:
        flash("Password cannot be blank!", 'red ')
        valid = False
    elif len(password) < 8:
        flash("Password must be at least 8 characters!", 'red ')
        valid = False
    elif not PW_REGEX.match(password):
        flash("Password is weak!", 'red')
        flash("What is a strong password?", 'message')
        valid = False
    elif confirm_pw != password:
        flash("hidden", "hidden")
        flash("Password doesn't match!", 'red')
        valid = False
    else:
        flash("hidden", "hidden")
    
    if valid:
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
        session.pop('dob')

        return render_template('results.html', first_name = first_name, last_name = last_name, dob = dob, email = email)
    else:
        return redirect('/')

@app.route('/home', methods=['POST'])

def redirect_url(default='display_index'):
    return redirect(url_for(default))

app.run(debug=True)