#Gets data after authentication
#Puts it into reddis
#Calls the functions that correspond to every operation
#Functions perform the operations and return a reddis key with the result
#Returns a reddis address with the computed query
#Sends the key to tornado. Tornado formalates the result and send it to client

# import redis
# from operations.query import query
import logging as logger
import pika
# import time
import json
from operations.query import query
logger.basicConfig(level=logger.DEBUG)
import messages

def onQuery(ch, method, props, body):
	try:
		ch.basic_ack(delivery_tag = method.delivery_tag)

		body = body.decode("utf-8")
		body = json.loads(body)

		userID = body.get("user_id", None)
		if userID is None: return

		queryDesc = body.get('query', None)
		if queryDesc is None: return

		data = query(queryDescription=queryDesc, userID=userID)
		response, http_code = messages.jsonify_message(
			dictify=True,
			message=messages.query_executed_successfully())

		response['data'] = data
		response = json.dumps(response)

	except Exception as err:
		response, http_code = messages.jsonify_message(message=err)

	ch.basic_publish(
		exchange = '',
		routing_key = props.reply_to,
		properties = pika.BasicProperties(
			correlation_id = props.correlation_id
		),
		body=response
	)


def main():
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host='localhost'),
	)
	channel = connection.channel()
	channel.queue_declare(queue='rpc_queue')
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(onQuery, queue='rpc_queue')
	print(" [x] Awaiting RPC requests")
	channel.start_consuming()

if __name__ == '__main__':
	main()