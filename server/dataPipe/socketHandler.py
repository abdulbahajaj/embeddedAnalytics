import json
import tornado.websocket
from pika.adapters.tornado_connection import TornadoConnection
import uuid
import pika
import logging as logger
from config import Config
import utils
from user import actions as user_actions

class RabbitMQConnection(object):
	__io_loop=None
	__connected=None
	__connecting=None
	__connection=None
	__channel=None
	__callback_queue = None
	def __init__(self, io_loop,):
		logger.debug('PikaClient: __init__')
		self.__io_loop=io_loop
		self.__connected=False
		self.__connecting=False
		self.__connection=None
		self.__channel=None
		self.connect=self.__connect
		self.call=self.__call

	def __connect(self):
		if self.__connecting:
			logger.debug('PikaClient: Already connecting to RabbitMQ')
			return

		logger.debug('PikaClient: Connecting to RabbitMQ')
		self.__connecting = True

		cred = pika.PlainCredentials(Config.RabbitMQ.username, 
								 Config.RabbitMQ.password)
		param = pika.ConnectionParameters(
			host=Config.RabbitMQ.host,
			port=Config.RabbitMQ.port,
			virtual_host=Config.RabbitMQ.virtual_host,
			credentials=cred
		)
		self.__connection = TornadoConnection(param,
							on_open_callback=self.__on_connected,
							stop_ioloop_on_close=False)

		self.__connection.add_on_close_callback(self.__on_close)

	def __on_connected(self, connection):
		logger.debug('PikaClient: connected to RabbitMQ')
		self.__connected = True
		self.__connection = connection
		self.__connection.channel(self.__on_channel_open)

	def __call(self,message,correlation_id):
		self.__channel.basic_publish(exchange='',
			routing_key='rpc_queue',
			properties=pika.BasicProperties(
				reply_to = self.__callback_queue,
				correlation_id = correlation_id,
			),
			body=str(message)
		)

	def __on_response(self, ch, method, props, body):
		print("I got",props.correlation_id)
		ClientWebSocket.on_response(message=body,correlation_id=props.correlation_id)

	def __on_close(self, connection):
		logger.debug('PikaClient: rabbit connection closed')
		self.__io_loop.stop()

	def __on_queue_open(self,a):
		self.__callback_queue = a.method.queue
		self.__channel.basic_consume(
			self.__on_response, 
			no_ack=True,
			queue=self.__callback_queue)

	def __on_channel_open(self, channel):
		# print("channel: ", channel)
		logger.debug('PikaClient: Channel %s open, Declaring exchange' % channel)
		self.__channel = channel

		result = self.__channel.queue_declare(
			callback=self.__on_queue_open,
			exclusive=True
		)

class ClientWebSocket(tornado.websocket.WebSocketHandler):
	client_handler = {}

	client_id = None

	permission = None

	company = None

	def open(self):
		self.client_id = utils.generate_id()
		while ClientWebSocket.client_handler.get(self.client_id,None) is not None:
			self.client_id = utils.generate_id()
		ClientWebSocket.client_handler[self.client_id] = self

		self.permission = dict(public_key=False, private_key=False)
		logger.debug("A Client Websocket established")
		print("Openned connection")

	def authenticate(self, creds):
		public_key = creds.get("public_key")

		company = user_actions.get_company_from_API_key(public_key = public_key)
		if company is not None:
			self.permission['public_key'] = True
			self.company = company
			print(self.company)


	def on_message(self, message):
		message = json.loads(message)
		message_type = message.get("type", None)
		if message_type is None: pass
		elif message_type == "auth":
			self.authenticate(creds = message.get('creds'))
		elif message_type == "query":
			message_id = message.get('id',None)
			data = message.get('data', None)
			correlation_id = self.client_id + ":" + message_id
			self.application.pc.call(message=data,correlation_id=correlation_id)

	@classmethod
	def on_response(cls,message,correlation_id):
		correlation_id = correlation_id.split(":")
		client_id = correlation_id[0]
		message_id = correlation_id[1]
		response = {'id': message_id, 'data': message.decode("utf-8")}
		cls.client_handler[client_id].write_message(response)

	def on_close(self):
		print("connection closed")
		logger.debug("connection closed")
		if self.client_id is None: return
		del ClientWebSocket.client_handler[self.client_id]
	
	def check_origin(self, origin):
	    return True




























































