import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")
db = cluster["Data"]
collection = db["Users"]

post = {"_id":0, "name": "tim","score":5}
post1 = {"_id":5, "name": "joe"}
post2 = {"_id":6, "name": "bill"}

collection.insert_many([post1,post2])



