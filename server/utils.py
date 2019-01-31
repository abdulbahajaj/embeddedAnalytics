import bcrypt
import uuid
import simplecrypt #import encrypt as simple_encrypt, decrypt as simple_decrypt

def generate_id():
	return ''.join([uuid.uuid4().hex for x in range(4)])

def hash(string):
	salt = bcrypt.gensalt()
	string = string.encode('utf8')
	string = bcrypt.hashpw(string, salt)
	return dict(string=string)

def check_hash(string, hashed_string):
	string = string.encode('utf8')
	if bcrypt.hashpw(string ,hashed_string) != hashed_string:
		return False
	return True

def encrypt(text, password):
	ciphertext = simplecrypt.encrypt(password, text)
	return dict(
		ciphertext=ciphertext
	)

def decrypt(ciphertext, password):
	text = simplecrypt.decrypt(password, ciphertext)
	return dict(
		text=text
	)


