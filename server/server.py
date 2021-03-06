import tornado.ioloop
import tornado.web
import json
import os
import logging as logger
from dataPipe.socketHandler import RabbitMQConnection, ClientWebSocket
from config import Config
import flask
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from schema import schema
from user import actions as user_actions
import messages

settings = dict(
	debug = True
)

# Setting application
application = tornado.web.Application(
	[(Config.SocketClient.path, ClientWebSocket),],
	**settings
)

app = flask.Flask(__name__)
app.secret_key = '''c05b9ea1593b432788cc24b256f7ae002c67382868bd42a8abba26d5f511d979c4cc07375b2e49c1b48e07283eae1868779eed047e874fd3a7cb7ea10b2ac5dd5bfe92c3c16e4b56a11e84f089853a7c277268f813564f0296871f056ee4ef0e7bee8f2e97d249408786dfeba3137256e3ca56a3ef794e2c889e5a469ab71eeec98ac93fc5704eb4ab4707ae8b70e3a23f3ea525c80a405397032ae68d0c73a3ddb357917a68434fa0b9c4953767bf0d9daeb72023784dffb5037130a01fae273add52a049e94f99ad173f2333af2f419eddda44436e4191be219bdcfc445c9d407c15aaddea4da88babd5abe4953b46bbe864cb3a3f4183a72b83f1af8c4a63d2cc2151570649229d51f7910fb60a2ceb62c85ee146495ba8f22f5b4fce5a7fb2976aa4548943558e3e48eb31b387198cbb2d5a097d464bb23d234f31b2a9f6e512689bdde64dcaa8b54303a3d4005c15c46f77d2d04eae8baaffb9a98a18ee047d5cdc7b074e08b6d1309f45725e83504a0c34cae34c92a25c0879d420f1ff331beb0a7c4748458cafc3beb46008e58868a92bd81742fa8c62425991f68bd6bea4f2a04ec442f8a2bd41fabb26a0812955a9bc02364332a87870fb096abfce6985c150a6dc44668de0f6b82df3ae03b9887bbd39244ea2bb5aa4b2470185b9f50b42a3507749398c3158d0c543a649640198834c594ff58228e424fea86d46335e86770ea64b978183e5841ed6a6eed693d3de59b347acac8389231cc81cdbb4bdab0ad9b94f4eab2b9ba0d39a8ffca8d246dbb57c4be984c994af2486a721b5dbee107c85480ba1bf08ffb444cef20f48a2d1b9054f44bf0431364deaf3207b69e51789c94598936fc21ab4315fdd87632e220d5c4175b3fd9fa294d3a2578e44bf209f794fe98c26f71ff9789a7e73af2d90c5724d2eb075caa1d9431f1b93bdc4dcd5494f9fb0f44e1e8e0bd96755c3bb55a4d0411f9b5c11ec48a5f9b32e6770c535e04959a49625f622beee61adaebdd5374740898a74b1b0bdf0695a0ec13618062d41538d46339957a140e9f6548ba4c7bc413eb140195b3762f578c8dc72df7b1f4245b4acca93859e1204f8757a36b83043a286c10bf9e56788d28cd541ea66394d788a5ea02ddc31f2fe5f7ba8724f5d4359b989c69184e0c1629900ad3349034214b64e463575409ade3788a2d34deb42c3bcf451fa41ee404acbb6edcccdd7461fbb8eee28e7a8653cc7f244599e244a85843c236fb2767bd40b37f4135caa414583e2b1fa1efbf76c3e520223b7584fed9dd9f87eac139f34a94f4e37afb94c379c76efc9b0f4b6dbdd45b7a7ad6b410b86ed9b4a0db8c6425fb751c54a754227bac1b5047dc37aa5adee4d11e4334034a39645960fa182f20fa97be8dbd443908acb9379d02fc147ea7ab9a765fc49d682ef4c5d58812c90e2e3eddfafd744e4bb362146d0c4f524641f040f31c14bb490c123813a8bf3f14b768f0571fa4825b9bff785dd86b4b0e30aeb5ecdd843839b1a6ab738792fa999550aada65f4c4f9e927eecf73d4f76df6e48a9381e4090b61c72f206083ebc46d1e278f2084b67855c9a88a556f45ae800e9dafea940d0a7ced3d98e9029859bcdc14affe04b918d600da46a737d1a2ec6de25aa7d4842b218dacfe3b132619d602e37eb8147cbbce1001b851cbfd7de43291435b8403a99b047621765220f864208c6be3f4488bbd53f636ff0b3c9c143cee94e7b45c8845e1b491d31f51d7e319ca194ed43a0b950d17df70e2e7016c99b43d3ef410f8dc8743b6983b4643b2aae3986fa47a5891643990f800c3617a991d4390147f8bf997ce5ab79dbd4b2d5eb5433fb4b58a41741ffc4fda6b1b7df5e28743b473baa88808c5bea65a5c7977beccf774adebba2503f04075e60732877842ab64cac8969501b2d45d8561d049b919d3e4db8a818441de63ee0a9c67bcfe4d819462d819cd55aaee133f900605f9a96d9484d8388ce2d59bd6cad5d8abc9f2402449c89a22b33608f4aa3aead3aae4cc34425a9938fb4704f2e92210ecf5b58654e9eb5a9c24f58e87ea285a73a93bc244992a379d52d307b8e1a4e8daee8f7e447b7985c23ff563f4b799ae80565894848bab71f0e67a00b3c825bed781f4a304fb3aae2c3bdcb6a3bcc405df26f1d114e41848a7c4e55448fcb891ca3e5936849dbb4ab20e0125571d348ea7765a3f1446a84b128ab55b68170cbeeb8b3a49847f0bdc9639566d66ad2'''

@app.route("/graphql")
def graphQL():
	try:
		try:
			user = user_actions.get_logged_user()
		except messages.user_not_logged_in:
			user = None
		query = flask.request.data.decode("utf-8")
		query = json.loads(query)
		query = query.get('query', None)
		if query is None:
			return "Please provide a query"
		result = schema.execute(query, context={"user": user})
		if result.errors is not None or result.data is None:
			errors = [str(error) for error in result.errors]
			errors = json.dumps(errors)
			return errors
		result = json.dumps(dict(result.data))
		return result
	except Exception as err:
		raise err
		return messages.jsonify_message(message=err)

def main():
	io_loop = tornado.ioloop.IOLoop.instance()

	pc = RabbitMQConnection(io_loop)
	application.pc = pc
	application.pc.connect()
	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(Config.Flask.port)

	application.listen(Config.SocketClient.port)
	try:
		io_loop.start()
	except KeyboardInterrupt:
		io_loop.stop()

if __name__ == "__main__":
    main()