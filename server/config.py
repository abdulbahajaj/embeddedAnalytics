class Config:
	class RabbitMQ:
		host='127.0.0.1'
		port=5672
		virtual_host='/'
		username='guest'
		password='guest'
		query_exchange="queries"
		publish_exchange="queries"
		exchange_type="direct"
	class SocketClient:
		path=r'/client'
		port=8888
	class Flask:
		port=80