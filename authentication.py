import secrets
import string

def generate_token():
	alphabet = string.ascii_letters + string.digits
	token = ''.join(secrets.choice(alphabet) for i in range(6))
	return token

def grind_salt():
	alphabet = string.ascii_letters + string.fixed_digits
	salt_str = ''.join(secrets.choice(alphabet) for i in range(16))
	return salt_str