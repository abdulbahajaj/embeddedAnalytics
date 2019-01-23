import tornado.ioloop
import tornado.web
import tornado.websocket
from pika.adapters.tornado_connection import TornadoConnection
import json
import uuid
import os
import pika
import logging as logger

# logger.basicConfig(level=logger.INFO√)

class Config:
	class RabbitMQ:
		host='127.0.0.1'
		port=5672
		virtualHost='/'
		username='guest'
		password='guest'
		queryExchange = "queries"
		publishExchange = "queries"
		exchangeType = "direct"

	class SocketClient:
		path=r'/client'
		port=8888

def generateSessionID():
	return uuid.uuid4().hex

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
			virtual_host=Config.RabbitMQ.virtualHost,
			credentials=cred
		)
		self.__connection = TornadoConnection(param,
							on_open_callback=self.__onConnected,
							stop_ioloop_on_close=False)

		self.__connection.add_on_close_callback(self.__onClosed)

	def __onConnected(self, connection):
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

	def __onClosed(self, connection):
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
	clientID = None
	def open(self):
		self.clientID = generateSessionID()
		while ClientWebSocket.client_handler.get(self.clientID,None) is not None:
			self.clientID = generateSessionID()
		ClientWebSocket.client_handler[self.clientID] = self
		logger.debug("A Client Websocket established")

	def on_message(self, message):
		print("message: ",message)
		message = json.loads(message)
		messageID = message.get('id',None)
		data = message.get('data', None)

		correlation_id = self.clientID + ":" + messageID
		print("correlation_id: ", correlation_id)
		self.application.pc.call(message=data,correlation_id=correlation_id)
		# logger.debug("Received message from " + self.clientID + ": " + message)

	@classmethod
	def on_response(cls,message,correlation_id):
		correlation_id = correlation_id.split(":")
		print("correlation_id: ", correlation_id)
		clientID = correlation_id[0]
		messageID = correlation_id[1]
		response = {'id': messageID, 'data': message.decode("utf-8")}

		print("client_handler: ",cls.client_handler)


		cls.client_handler[clientID].write_message(response)

	def on_close(self):
		print("connection closed")
		logger.debug("connection closed")
		if self.clientID is None: return
		del ClientWebSocket.client_handler[self.clientID]
	
	def check_origin(self, origin):
	    return True

# Setting directories
settings = dict(
	# template_path = os.path.join(os.path.dirname(__file__), "templates"),
	# static_path = os.path.join(os.path.dirname(__file__), "static"),
	debug = True
)

# Setting application
application = tornado.web.Application(
	[(Config.SocketClient.path, ClientWebSocket),],
	**settings
)

# Main
def main():
	logger.debug("Starting server")
	io_loop = tornado.ioloop.IOLoop.instance()

	pc = RabbitMQConnection(io_loop)
	application.pc = pc
	application.pc.connect()
	# print(pc.call())

	application.listen(Config.SocketClient.port)
	try:
		io_loop.start()
	except KeyboardInterrupt:
		io_loop.stop()

if __name__ == "__main__":
    main()























