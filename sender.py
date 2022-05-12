import smtplib
import ssl
from config import config
from connect import fetch_email
from connect import fetch_auth_code

def send_email(username):
	context = ssl.create_default_context()
	params = config('config.ini', 'email')
	user_email = fetch_email(username)
	sender = params.get('user')
	sender_pass = params.get('password')
	code = fetch_auth_code(username)
	message = """\
	Subject: Authenticate Login

	Your Authentication Code is: {0}""".format(code)

	if user_email == None:
		return False

	with smtplib.SMTP_SSL("smtp.gmail.com", port=params.get('port'), context=context) as server:
		server.login(sender, sender_pass)
		server.sendmail(sender, user_email, message)

	return True