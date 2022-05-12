from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from markupsafe import escape
from connect import login_attempt
from connect import sign_up_attempt
from connect import auth_attempt
from authentication import generate_token
from sender import send_email
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
		return do_the_login(user, pw)
	else:
		return show_login_form()

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = request.form['user2']
		pw = request.form['pwnew']
		pw2 = request.form['pw2']
		email = request.form['email']
		return do_the_sign_up(user, pw, pw2, email)
	else:
		return show_sign_up_form()

@app.route('/auth/<user>', methods=['GET', 'POST'])
def auth_user(user):
	if request.method == 'POST':
		auth = request.form['auth']
		return do_the_auth(user, auth)
	else:
		return show_auth_form(user)

@app.route('/user/<user>', methods=['GET'])
def user(user):
	return render_template('user.html', name=user)


def do_the_auth(username, auth_code):
	auth = auth_attempt(username, auth_code)
	if auth:
		print('Authenticated.')
		return redirect(url_for('user', user=username))
	else:
		error = 'Authentication failed. A new authentication code has been sent to your e-mail address.'
		send_email(username)
		return render_template('auth.html', user=username, error=error)


def do_the_login(user, pw):
	login = login_attempt(user, pw)
	print(login)
	if login:
		print('Login is a go!')
		send_email(user)
		return redirect(url_for('auth_user', user=user))
	else:
		error = 'Invalid username/password. Please try again.'
		print(error)
		return render_template('login.html', error=error)

def do_the_sign_up(user, pw, pw2, email):
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

		sign = sign_up_attempt(user, pw, email)
		if sign:
			print('Sign up is a go!')
			return redirect(url_for('login'))
		else:
			error = 'That username/email is already taken.'
			return render_template('sign-up.html', error=error)

def show_login_form():
	return render_template('login.html')

def show_sign_up_form():
	return render_template('sign-up.html')

def show_auth_form(user):
	return render_template('auth.html', user=user)

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
