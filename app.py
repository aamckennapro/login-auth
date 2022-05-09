from flask import Flask
from flask import request
from flask import render_template
from markupsafe import escape
from connect import login_attempt
from connect import sign_up_attempt
import re

app = Flask(__name__)

@app.route('/')
def index():
	return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = request.form['user']
		pw = request.form['pw']
		print("Woo!")
		return do_the_login(user, pw)
	else:
		print("Boo!")
		return show_login_form()

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = request.form['user2']
		pw = request.form['pwnew']
		pw2 = request.form['pw2']
		return do_the_sign_up(user, pw, pw2)
	else:
		return show_sign_up_form()

def do_the_login(user, pw):
	login = login_attempt(user, pw)
	print(login)
	if login:
		print('Login is a go!')
		return render_template('user.html', name=user)
	else:
		error = 'Invalid username/password. Please try again.'
		print(error)
		return render_template('login.html', error=error)

def do_the_sign_up(user, pw, pw2):
	if pw != pw2:
		error = 'Passwords must match.'
		return render_template('sign-up.html', error=error)
	else:
		if len(pw) < 8 or len(pw) > 16:
			error = 'Password must be between 8-16 characters in length.'
			return render_template('sign-up.html', error=error)

		if len(user) < 5 or len(user) > 16:
			error = 'Username must be between 5-16 characters in length.'
			return render_template('sign-up.html', error=error)

		if not char_search_in_string(pw):
			error = 'Password must include at least one letter.'
			return render_template('sign-up.html', error=error)

		if not num_search_in_string(pw):
			error = 'Password must include at least one number.'
			return render_template('sign-up.html', error=error)

		if not symbol_search_in_string(pw):
			error = 'Password must include at least one symbol.'
			return render_template('sign-up.html', error=error)

		if symbol_search_in_string(user):
			error = 'Username may not include any non-alphanumeric characters.'
			return render_template('sign-up.html', error=error)

		sign = sign_up_attempt(user, pw)
		if sign:
			print('Sign up is a go!')
			return render_template('user.html', name=user)
		else:
			error = 'That username is already taken.'
			return render_template('sign-up.html', error=error)

def show_login_form():
	return render_template('login.html')

def show_sign_up_form():
	return render_template('sign-up.html')

def char_search_in_string(pw):
	search = re.search('[A-Za-z]+', pw)
	if search:
		return True
	else:
		return False

def num_search_in_string(pw):
	search = re.search('[0-9]+', pw)
	if search:
		return True
	else:
		return False

def symbol_search_in_string(pw):
	search = re.search('[^A-Za-z0-9]', pw)
	if search:
		return True
	else:
		return False
