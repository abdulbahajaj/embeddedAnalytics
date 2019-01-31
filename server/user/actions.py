import flask
from . import models
import utils
import time
import redis
import json
import messages

redisConnection = redis.Redis(
	host='localhost',
	port=6379)

def get_company_from_API_key(public_key, private_key=None):
	company = models.Company.objects(public_key=public_key)
	if len(company) != 1:
		return None

	if private_key is not None:
		if not utils.check_hash(private_key ,company.private_key_hash):
			return None

	return company[0]

def get_private_key(password, user):

	if not utils.check_hash(password ,user.password_hash):
		return None

	company_key = utils.decrypt(
		ciphertext=user.company_key_encrypted, 
		password=password
	)

	company = user.company

	private_key = utils.decrypt(
		ciphertext=company.private_key_encrypted, 
		password=company_key)

	return private_key

def generate_keys(company, password):
	company_id = str(company.id)

	company_key = utils.generate_id()
	company_key_encrypted = utils.encrypt(text=company_key, password=password)

	public_key = company_id + "_" + utils.generate_id()

	private_key  = company_id + "_" + utils.generate_id()
	private_key_hash = utils.hash(string=private_key)
	private_key_encrypted = utils.encrypt(text=private_key, password=company_key)


	password_hash = utils.hash(string=password)

	return dict(
		public_key = public_key,
		company_key_encrypted = company_key_encrypted,
		private_key_hash = private_key_hash,
		private_key_encrypted = private_key_encrypted,
		password_hash = password_hash
	)

def register(email, password):
	if len(models.User.objects(email=email)) > 0:
		raise messages.user_exists()

	company = models.Company()
	company.created = time.time()
	company.save()

	keys = generate_keys(company=company, password=password)

	company.public_key = keys.get('public_key')
	company.private_key_hash = keys.get('private_key_hash').get('string')
	company.private_key_encrypted = keys.get('private_key_encrypted').get("ciphertext")
	company.save()

	user = models.User()
	user.company = company
	user.email = email
	user.created = time.time()
	user.company_key_encrypted = keys.get('company_key_encrypted').get("ciphertext")
	user.password_hash = keys.get('password_hash').get('string')
	user.save()

	login(email=email, password=password)

	return user

def logout():
	session_id = flask.session.get('id',None)
	if session_id is None: return messages.user_logged_out()
	del flask.session['id']
	redisConnection.delete("session:" + session_id)
	return messages.user_logged_out()

def login(email, password):
	logout()
	user = models.User.objects(email=email)
	if len(user) != 1:
		raise messages.user_not_found()
	user = user[0]
	if not utils.check_hash(string=password, hashed_string=user.password_hash):
		raise messages.user_not_found()

	session_id = utils.generate_id()

	while redisConnection.get("session:" + session_id) is not None:
		session_id = utils.generate_id()


	flask.session['id'] = session_id
	session_content = {"user_id": str(user.id)}
	session_content = json.dumps(session_content)
	redisConnection.set("session:" + session_id, session_content)

	return user

def get_logged_user():
	session_id = flask.session.get('id',None)
	if session_id is None: 
		raise messages.user_not_logged_in()

	user = redisConnection.get("session:" + session_id)
	if user is None:
		logout()
		raise messages.user_not_logged_in()

	try:
		user = json.loads(user)
	except:
		logout()
		raise messages.user_not_logged_in()

	user_id = user.get("user_id", None)
	if user_id is None:
		logout()
		raise messages.user_not_logged_in()

	user = models.User.objects(id = user_id)
	if len(user) != 1:
		logout()
		raise messages.user_not_logged_in()

	return user[0]







