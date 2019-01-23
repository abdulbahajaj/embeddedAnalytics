from operations.search import search
from operations.select import select
import uuid
from errors import WrongOperationType, NoArgsGiven, MissingOperationType, NoInputGiven

operationsHash = {}
operationsHash['select'] = select
operationsHash['search'] = search

def query(queryDescription):
	"""
	Processes the query description and returns a list containing the query result

	:param queryDescription: A list of dictionary that describes operations dict(operation={operationType}, **operation_args)
	
	:raises WrongOperationType: when a given operation is not identified
	:raises MissingOperationType: when no operation type was given

	:returns: None
	"""

	outputData = []
	userID = None
	collectionID = None

	for operationDescription in queryDescription:

		opType = operationDescription.get('operation', None)
		assert opType is not None, MissingOperationType()
		del operationDescription['operation']

		if opType == 'select':
			userID = operationDescription.get('userID', None)
			collectionID = operationDescription.get('collectionID', None)
			print(userID,collectionID)

		operation = operationsHash.get(opType,None)
		assert operation is not None,WrongOperationType(context=dict(opType=opType))

		outputData = operation(inputData=outputData, **operationDescription)

	return outputData




































