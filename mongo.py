import pymongo
from pymongo import MongoClient

import os

# import pandas
# import pandas as pd

cluster = pymongo.MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")

post = {"_id":0, "name": "tim","score":5, "Major":0}
post1 = {"_id":5, "name": "joe"}
post2 = {"_id":6, "name": "bill"}

#local_dir = os.getcwd()

#Para torvic

#table = pd.read_csv(f'{local_dir}/ClasesFinalFINAL.csv')
# print(table)

db = cluster['MayorsDatabase']
collection = db["Ambiente Construido"]

myquery = {"CarreraID": 0 }
mydoc = collection.find(myquery)

for i in mydoc:
    print(i['class'])

# for i in range(0,9,1):
#     print(" ")
#     print(table.columns[i])
#     collection = db[f'{table.columns[i]}']
#     num = 0
#     for j in range(0, table.count(axis='columns')[i], 1):
#         print(table.iloc[j][i])
#         post = {"CarreraID":i,"ClassID":num,"Mayor":table.columns[i],"class":table.iloc[j][i],}
#         collection.insert_one(post)
#         num = num+1


