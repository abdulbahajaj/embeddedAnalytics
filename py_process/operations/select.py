from data import pull

def select(collectionID,userID,timeIntervalStart=None,timeIntervalEnd=None,inputData=[]):
	"""
	Selects data from a given collection

	:param collectionID: the id of the collection that is going to be selected from
	:param userID: the id of the user that owns the collection
	:param timeIntervalStart: the time interval that the partition should be selected from
	:param timeIntervalEnd: the time interval that the partition should be ended in
	:param inputData: should be ignored. added it to be consistent with the interface with other operations

	:returns: a list of results that are selected
	"""

	return pull(
		collectionID=collectionID,
		userID=userID,
		timeIntervalStart=timeIntervalStart,
		timeIntervalEnd=timeIntervalEnd
	)