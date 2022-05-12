import secrets
import string

def generate_token():
	alphabet = string.ascii_letters + string.digits
	token = ''.join(secrets.choice(alphabet) for i in range(6))
	return token