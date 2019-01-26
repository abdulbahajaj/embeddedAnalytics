from operations.search import search
from operations.select import select
import uuid
from errors import WrongOperationType, NoArgsGiven, MissingOperationType, NoInputGiven

operationsHash = {}
operationsHash['select'] = select
operationsHash['search'] = search

def query(queryDescription, userID):
	"""
	Processes the query description and returns a list containing the query result

	:param queryDescription: A list of dictionary that describes operations dict(operation={operationType}, **operation_args)
	
	:raises WrongOperationType: when a given operation is not identified
	:raises MissingOperationType: when no operation type was given

	:returns: None
	"""

	outputData = []

	for operationDescription in queryDescription:

		opType = operationDescription.get('type', None)
		assert opType is not None, MissingOperationType()
		del operationDescription['type']

		operation = operationsHash.get(opType,None)
		assert operation is not None,WrongOperationType(context=dict(opType=opType))

		outputData = operation(
			inputData=outputData, 
			userID=userID, 
			**operationDescription)

	return outputData




































