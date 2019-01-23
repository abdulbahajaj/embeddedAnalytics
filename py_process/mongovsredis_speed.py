#!/usr/bin/env python2.7
import random
import sys, time
from pymongo import MongoClient as Connection
import redis
import uuid
import json
# connect to redis & mongodb
redis = redis.Redis()
mongo = Connection().test
collection = mongo[uuid.uuid4().hex]
collection.ensure_index('key', unique=True)

collection2 = mongo[uuid.uuid4().hex]

listKey = uuid.uuid4().hex

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


def mongo_set(data,dataList):
    for k, v in data.items():
        collection.insert({'key': k, 'value': v})

def mongo_get(data,dataList):
    for k in data.keys():
        val = collection.find_one({'key': k}).get('v')

def redis_set(data,dataList):
    for k, v in data.items():
        redis.set(k, v)

def redis_get(data,dataList):
    for k in data.keys():
        val = redis.get(k)

def mongo_list_get(data,dataList):
    counter = 0
    for x in collection2.find({}):
        pass
        # counter += 1
    # print("mongo",counter)
    # collection.insert_many(dataList)

def mongo_list_insert(data,dataList):
    collection2.insert_many(dataList)

def redis_list_get(data,dataList):
    counter = 0
    l = json.loads(redis.get(listKey))
    # for x in l:
    #     counter += 1
    # print("redis",counter)

def redis_list_insert(data,dataList):
    redis.set(listKey, json.dumps(dataList))
    # for item in dataList:
    #     redis.xadd(name=listKey,fields=item)

def getDummyData():
    userID = "dummy"
    collectionID = "student"

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
    data = []
    for item in range(1000000):
        data.append(dict(
            timestamp = time.time(),
            gpa=random.randint(1, 4),
            age=random.randint(17, 28),
            major=random.choice(majors),
            name = random.choice(names) + " " + random.choice(names),
        ))

    return data

def do_tests(num, tests):
    # setup dict with key/values to retrieve
    data = {'key' + str(i): 'val' + str(i)*100 for i in range(num)}

    dataList = getDummyData()
    print("dataset")
    # run tests
    for test in tests:
        start = time.time()        
        test(data=data,dataList=json.loads(json.dumps(dataList)))
        elapsed = time.time() - start

        print( "Completed %s: %d ops in %.2f seconds : %.1f ops/sec" % (test.__name__, num, elapsed, num / elapsed) )

if __name__ == '__main__':
    num = 1000 if len(sys.argv) == 1 else int(sys.argv[1])
    tests = [
        mongo_set, 
        mongo_get, 
        redis_set, 
        redis_get,
        mongo_list_insert,
        mongo_list_get,
        redis_list_insert,
        redis_list_get] # order of tests is significant here!
    do_tests(num, tests)


































































