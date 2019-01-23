def search(inputData,filter={}):
	"""
	Performs search on the content. 

	:param inputData: the data that the input operation will be compared against.
	:param filter: a dictionary that will be compared against all the input data.

	:returns: the results of the search
	"""

	output = []
	for item in inputData:
		for key in filter:
			if item.get(key,None) == filter.get(key,None):
				output.append(item)
	return output