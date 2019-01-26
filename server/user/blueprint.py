from . import actions
import flask
import json

def register():
	data = json.loads(flask.request.data)
	print(data)
	email = data.get('email')
	password = data.get('password')
	actions.register(email=email, password=password)
	return "bahajaj is amazing"

def get_blueprint():
	bp = flask.Blueprint("user", __name__, url_prefix="/user" )
	bp.route("/register", methods=['POST'])(register)
	return bp




