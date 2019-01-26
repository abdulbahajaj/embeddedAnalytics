from data import insert
import redis
import time
import random
def createDummyData(userID,collectionID,sampleSize):
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
	) for x in range(sampleSize)]

	insert(userID=userID,collectionID=collectionID,data=data)


def main():
	createDummyData(userID="5c4aae274cd635708233e8dc", collectionID="dummy", sampleSize=10000)



if __name__ == "__main__":
	main()