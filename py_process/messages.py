import json

def define_status(status_map, http_code, human_code):
	status_map[human_code] = http_code

STATUS_MAP = dict()

define_status(
	status_map = STATUS_MAP,
	http_code = 200,
	human_code = "success")

define_status(
	status_map = STATUS_MAP,
	http_code = 401,
	human_code = "unauthorized")

define_status(
	status_map = STATUS_MAP,
	http_code = 409,
	human_code = "conflict")

define_status(
	status_map = STATUS_MAP,
	http_code = 404,
	human_code = "not-found")

define_status(
	status_map = STATUS_MAP,
	http_code = 400,
	human_code = "bad-request")

define_status(
	status_map = STATUS_MAP,
	http_code = 500,
	human_code = "unknown-error")

def define_message(status ,message):
	http_code = STATUS_MAP.get(status,None)
	assert http_code is not None
	class ExceptionTemplate(Exception):
		message = None
		human_code = None
		http_code = None
		def __init__(self):
			super().__init__(self.message)

	ExceptionTemplate.message=message
	ExceptionTemplate.human_code=status
	ExceptionTemplate.http_code=http_code
	ExceptionTemplate.__name__ = status
	return ExceptionTemplate



def jsonify_message(message,dictify=False):
	try:
		response = dict(
			message = message.message,
			code = message.human_code,
		)
		http_status = message.http_code
		if dictify is not True:
			response = json.dumps(response)
	except:
		response, http_status = jsonify_message(
			message=unknown_error, 
			dictify=dictify)
	return response, http_status

unknown_error = define_message(status="unknown-error", message="An unknown error has occured. Our team is working on it")

''' Define messages here '''

collection_not_found = define_message(
	status="not-found", 
	message="Collection is not found")

user_not_found = define_message(
	status="not-found", 
	message="User is not found")

missing_query_type = define_message(
	status="bad-request", 
	message="The given query is missing a query type")


wrong_query_type = define_message(
	status="bad-request", 
	message="You have provided a wrong query type")


query_executed_successfully = define_message(
	status="success", 
	message="Your query has been executed successfully")