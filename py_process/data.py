import uuid
import time
import redis
import ujson as json
# import json
# import rapidjson as json

redisConnection = redis.Redis(
	host='localhost',
	port=6379)

def set(key,data): 
	'''
	Sets the data to the given hash key

	:param key: The location that the data is stored in
	:param data: The data that is going to be stored in the hash

	:returns: true if the operation was successful
	'''
	if isinstance(data,list):
		data = json.dumps(data)
	redisConnection.set(key,data)
	return True

def get(key,parse=True): 
	'''
	Retrieve the data stored in the given key

	:param key: The key that the data is stored in
	:param parse: Indicated whether or not the data should be parsed before it is returned or just returned as it

	:returns: The value inside the given key
	'''
	values = redisConnection.get(key)

	if parse is True:
		return parser(data=values)
	return values

def exists(key):
	'''
	Indicates whether or not there is a value stored inside the given hash key

	:param key: The key that is going to be examined

	:returns: True if there is a value stored inside the given key and False otherwise
	'''

	return redisConnection.exists(key)

def increment(key,amount=1):
	'''
	Atomically increment the integer value that is stored inside the given hash key

	:param key: The key that the data is stored in
	:param amount: The amount by which the value should be incremented by. Default is 1

	:returns: True
	'''

	redisConnection.incr(key,amount=amount)
	return True

def serializer(data,append=False):
	'''
	Serializes a given list

	:param data: The data that is going to be serialized
	:param append: Whether or not the data is going to be appended to an existing list or is it a new list

	:returns: Returns the serialized data as a string
	'''

	data = json.dumps(data)[1:-1]
	if append:
		data = "," + data
	return data

def parser(data):
	'''
	Serializes a given list

	:param data: the data that is need to be parsed

	:returns: list that is the result of the parsed string
	'''


	if data is None:
		data = ""

	try:
		data = int(data)
		return data
	except:
		pass

	if not isinstance(data,str):
		data = data.decode("utf-8")

	try:
		data = json.loads("[" + data + "]")
	except:
		pass

	return data

def append(key,data):
	'''
	Atomically append the given string to the given key

	:param data: a string that represent the serialized data

	:returns: None
	'''

	redisConnection.append(key,data)

def getCollectionKeys(userID,collectionID):
	'''
	Get the redis addresses that is associated with given collection

	:param userID: the user id
	:param collectionID: the collection id

	:returns: a dictionary that contains all the addresses
	'''

	main = userID + ":collections:" + collectionID + ":"
	exists = main + "exists"
	count = main + "count"

	partition =  main + "partition:"
	partitionCount = partition + "count"
	partitionList = partition + "list"
	partitionData = partition + "data:"

	currentPartion = partition + "current:"
	currentPartitionCount = currentPartion + "count"
	currentPartitionAddress = currentPartion + "address"

	return dict(
		main=main,
		exists=exists, #Detects whether or not a collection exists
		count=count,  #Count of all data entries in the collection (len(collection))
		partition = dict(
			main=partition, 	  #The main address for partitions
			count=partitionCount, #The number of existing partitions
			list=partitionList,   #List of existing partitions
			data=partitionData,   #The address that contain the actual partition data
			current=dict(
				main=currentPartion, 			 #The main address for partitions
				count=currentPartitionCount,	 #The number of data within the existing partitions
				address=currentPartitionAddress, #The address for the data contained within the current partition
	)))

def createPartition(collectionKeys,appended=True):
	'''
	Creates a partition that the data is stored in

	:param collectionKeys: the given collection keys
	:param appended: whether or not this is the first collection

	:returns: the address for the new partition
	'''

	address = str(int(time.time() * 1000))
	partition = serializer(data=[address],append=appended)
	address = collectionKeys.get('partition').get('data') + address

	#Append the address of the partition to the stored addresses
	if appended is True:
		append(key=collectionKeys.get('partition').get('list'),data=partition)
	else:
		set(key=collectionKeys.get('partition').get('list'),data=partition)


	#Increment the count of existing partitions
	increment(key=collectionKeys.get('partition').get('count'))

	#Set the address of the current partition to the address of the new partition and set the count of elements within the partition to 0
	set(collectionKeys.get('partition').get('current').get('address'),address)
	set(collectionKeys.get('partition').get('current').get('count'),0)
	return address

def updateWritingPartition(collectionKeys):
	'''
	creates a new partition when the size of the current partition is exceeded

	:param collectionKeys: the keys for the collection

	:returns: None
	'''
	
	currentCount = get(key=collectionKeys.get("partition").get("current").get("count"))

	if currentCount > 100000:
		address = createPartition(collectionKeys=collectionKeys)

'''Exposed interface'''
def createCollection(collectionKeys):
	'''
	creates a new collection

	:param collectionKeys: the keys for the collection

	:returns: None
	'''

	set(key=collectionKeys.get('exists'),data="True")
	set(key=collectionKeys.get('count'),data=0)
	createPartition(collectionKeys,appended=False)

def deleteCollection(userID,collectionID):
	'''
	deletes a collection

	:param userID: The user id of the user that owns the collection
	:param collectionID: The id of the collection

	:returns: None
	'''

	collectionKeys = getCollectionKeys(userID=userID,collectionID=collectionID)

	for key in redisConnection.scan_iter(collectionKeys.get('main') + "*"):
		redisConnection.delete(key)

def insert(userID,collectionID,data):
	"""
	Insert data to a collection

	:param userID: unique string that identifies the user
	:param collectionID: unique string that identifies the collection
	:param data: a list of data points to be appended to a given collection

	:returns: True if the operation was completed correctly
	"""
	collectionKeys = getCollectionKeys(userID=userID,collectionID=collectionID)

	if not exists(key=collectionKeys.get('exists')):
		createCollection(collectionKeys)

	updateWritingPartition(collectionKeys=collectionKeys)

	key = get(key=collectionKeys.get('partition').get('current').get('address'))

	insertCount = len(data)


	currentCount = get(key=collectionKeys.get('partition').get('current').get('count'))

	data = serializer(data=data,append=(not currentCount == 0))

	append(key=key,data=data)
	increment(key=collectionKeys.get('partition').get('current').get('count'),amount=insertCount)
	increment(key=collectionKeys.get('count'),amount=insertCount)

def pull(userID,collectionID,timeIntervalStart=None, timeIntervalEnd=None):
	"""
	pulls data from a given collection

	:param userID: unique string that identifies the user
	:param collectionID: unique string that identifies the collection
	:param timeIntervalStart: an optional time selector that identifies interval start 
	:param timeIntervalEnd: an optional time selector that identifies interval end

	:returns: a list of data
	"""

	collectionKeys = getCollectionKeys(userID=userID,collectionID=collectionID)
	partitionList = get(key=collectionKeys.get('partition').get('list'))
	basePartitionDataPath = collectionKeys.get('partition').get('data')

	if not exists(key=collectionKeys.get('exists')):
		#raise exception
		return []

	if timeIntervalStart is None:
		timeIntervalStart = int(partitionList[0])
	if timeIntervalEnd is None:
		timeIntervalEnd = int(partitionList[len(partitionList)-1])
	result = []
	for partition in partitionList:
		partition = int(partition)
		if partition < timeIntervalStart or partition > timeIntervalEnd:
			continue
		result += get(key=basePartitionDataPath + str(partition),parse=True)

	return result


















































