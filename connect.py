import psycopg2
from config import config

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
		return True
	else:
		return False

def sign_up_attempt(username, password):
	conn = None
	user = None
	try:
		params = config()
		print('Connecting to login')
		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		cur.execute('SELECT username FROM login WHERE username=\'{0}\';'.format(username))
		user = cur.fetchone()

		if user != None:
			cur.close()
			conn.close()
			print('Database connection closed.')
			return False

		else:
			cur.execute('INSERT INTO login (username, password) VALUES (\'{0}\', \'{1}\');'.format(username, password))
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