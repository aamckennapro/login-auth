import psycopg2
from config import config
from authentication import generate_token

def login_attempt(username, password):
	conn = None
	user = None
	try:
		params = config()
		print('Connecting to login.')
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print('Connected.')
		print('Trying user {0} and pass {1}.'.format(username, password))
		cur.execute('SELECT username FROM login where username=\'{0}\' and password=\'{1}\';'.format(username, password))

		user = cur.fetchone()
		#print(user[0])

		cur.close()
		conn.close()
		print('Database connection closed.')
		return login(user[0], username)
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	else:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def login(attempt, username):
	if attempt == username:
		conn = None
		try:
			params = config()
			conn = psycopg2.connect(**params)
			cur = conn.cursor()

			cur.execute('DELETE FROM auth WHERE username=\'{0}\';'.format(username))
			conn.commit()
			code = generate_token()
			cur.execute('INSERT INTO auth (username, auth_code) VALUES (\'{0}\', \'{1}\');'.format(username, code))
			conn.commit()
			cur.close()
			conn.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		else:
			if conn is not None:
				conn.close()
				print('Database connection closed.')
		return True
	else:
		return False

def sign_up_attempt(username, password, email):
	conn = None
	user = None
	email_check = None
	code = None
	try:
		params = config()
		print('Connecting to login')
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		cur.execute('SELECT username FROM login WHERE username=\'{0}\';'.format(username))
		user = cur.fetchone()
		cur.execute('SELECT email FROM login WHERE email=\'{0}\';'.format(email))
		email_check = cur.fetchone()

		if user != None:
			cur.close()
			conn.close()
			print('Database connection closed.')
			return False

		elif email_check != None:
			cur.close()
			conn.close()
			print('Database connection closed.')
			return False

		else:
			#print(username, password, email)
			cur.execute('INSERT INTO login (username, password, email) VALUES (\'{0}\', \'{1}\', \'{2}\');'.format(username, password, email))
			conn.commit()
			code = generate_token()
			cur.execute('INSERT INTO auth (username, auth_code) VALUES (\'{0}\', \'{1}\');'.format(username, code))
			conn.commit()
			cur.close()
			conn.close()
			print('Database connection closed.')
			return True
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	else:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def fetch_email(username):
	conn = None
	email = None
	try: 
		params = config()
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		cur.execute('SELECT email FROM login WHERE username=\'{0}\';'.format(username))
		email = cur.fetchone()

		cur.close()
		conn.close()
		print('Database connection closed.')
		if email == None:
			return None

		else:
			return email
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	else:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def fetch_auth_code(username):
	conn = None
	auth_code = None
	try: 
		params = config()
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		cur.execute('SELECT auth_code FROM auth WHERE username=\'{0}\';'.format(username))
		auth_code = cur.fetchone()

		cur.close()
		conn.close()
		print('Database connection closed.')
		if auth_code == None:
			return None

		else:
			return auth_code[0]
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	else:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def auth_attempt(username, code):
	conn = None
	auth_code = None
	try:
		params = config()
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		cur.execute('SELECT auth_code FROM auth WHERE username=\'{0}\';'.format(username))
		auth_code = cur.fetchone()

		if auth_code[0] == None:
			cur.execute('DELETE FROM auth WHERE username=\'{0}\';'.format(username))
			conn.commit()
			new_code = generate_token()
			cur.execute('INSERT INTO auth (username, auth_code) VALUES (\'{0}\', \'{1}\');'.format(username, new_code))
			conn.commit()
			return False

		elif auth_code[0] != code:
			cur.execute('DELETE FROM auth WHERE username=\'{0}\';'.format(username))
			conn.commit()
			new_code = generate_token()
			cur.execute('INSERT INTO auth (username, auth_code) VALUES (\'{0}\', \'{1}\');'.format(username, new_code))
			conn.commit()
			return False

		else:
			return True
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	else:
		if conn is not None:
			conn.close()
			print('Database connection closed.')






