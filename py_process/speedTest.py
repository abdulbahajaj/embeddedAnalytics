import time
import uuid
import random
from data import insert, deleteCollection,pull
from operations.query import query

__sampleSize__ = 90000

def createDummyData(userID,collectionID):
	names = ["Aaberg","Aalst","Aara","Aaren","Aarika","Aaron","Aaronson","Ab","Aba","Abad","Abagael","Abagail","Abana",
		"Abate","Abba","Abbate","Abbe","Abbey","Abbi","Abbie","Abbot","Abbotsen","Abbotson","Abbotsun","Abbott","Abbottson",
		"Abby","Abbye","Abdel","Abdella","Abdu","Abdul","Abdulla","Abe","Abebi","Abel","Abelard","Abell","Abercromby","Abernathy",
		"Abernon","Abert","Abeu","Abey","Abie","Abigael","Abigail","Abigale","Abijah","Abisha","Abisia","Abixah","Abner","Aborn",
		"Abott","Abra","Abraham","Abrahams","Abrahamsen","Abrahan","Abram","Abramo","Abrams","Abramson","Abran","Abroms","Absa",
		"Absalom","Abshier","Acacia","Acalia","Accalia","Ace","Acey","Acherman","Achilles","Achorn","Acie","Acima","Acker",
		"Ackerley","Ackerman","Ackler","Ackley","Acquah","Acus","Ad","Ada","Adabel","Adabelle","Adachi","Adah","Adaha","Adai",
		"Adaiha","Adair","Adal","Adala","Adalai","Adalard","Adalbert","Adalheid","Adali","Adalia","Adaliah","Adalie","Adaline",
		"Adall","Adallard","Adam","Adama","Adamec","Adamek","Adamik","Adamina","Adaminah","Adamis","Adamo","Adamok","Adams",
		"Adamsen","Adamski","Adamson","Adamsun","Adan","Adao","Adar","Adara","Adaurd","Aday","Adda","Addam","Addi","Addia"
		,"Addie","Addiego","Addiel","Addis","Addison","Addy","Ade","Adebayo","Adel","Adela","Adelaida","Adelaide","Adelaja"
		,"Adelbert","Adele","Adelheid","Adelia","Adelice","Adelina","Adelind","Adeline","Adella","Adelle","Adelpho","Adelric",
		"Adena","Ader","Adest","Adey","Adham","Adhamh","Adhern","Adi","Adiana","Adiel","Adiell","Adigun","Adila","Adim","Adin"]
	

	majors = [
		"software engineering",
		"computer science",
		"electrical engineering",
		"civil engineering",
		"mechanical engineering",
		"life sciences",
		"humanities",
		"law",
	]

	data = [dict(
		timestamp = time.time(),
		gpa=random.randint(1, 4),
		age=random.randint(17, 28),
		major=random.choice(majors),
		name = random.choice(names) + " " + random.choice(names),
	) for x in range(__sampleSize__)]

	insert(userID=userID,collectionID=collectionID,data=data)

def deleteDummyData(userID,collectionID):
	# pass
	deleteCollection(userID=userID,collectionID=collectionID)

def pullData(userID,collectionID):
	pull(userID=userID,collectionID=collectionID)

def queryData_select(userID,collectionID):
	queryDescription = [
		dict(operation='select',collectionID=collectionID,userID=userID),
	]

	query(queryDescription=queryDescription)


def queryData_filter(userID,collectionID):
	queryDescription = [
		dict(operation='select',collectionID=collectionID,userID=userID),
		dict(operation='search',equal=dict(major='software engineering'))
	]

	print(len(query(queryDescription=queryDescription)))



def emptyTest(userID,collectionID):
	pass

if __name__ == '__main__':
	tests = [
		emptyTest,
		createDummyData,
		createDummyData,
		createDummyData,
		createDummyData,
		pullData,
		queryData_select,
		queryData_filter,
		deleteDummyData,
	]

	userID = "test_userID_" + uuid.uuid4().hex + uuid.uuid4().hex
	collectionID = "test_collection_" + uuid.uuid4().hex + uuid.uuid4().hex

	for test in tests:
		start = time.time()
		test(userID=userID,collectionID=collectionID)
		print("===========> ",test.__name__ , " = " ,time.time() - start)























