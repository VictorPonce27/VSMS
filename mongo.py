import pymongo
from pymongo import MongoClient

import os

import pandas as pd

cluster = MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")


local_dir = os.getcwd()

table = pd.read_csv(f'{local_dir}/ClasesFinalFINAL.csv')
print(table)

db = cluster['MayorsDatabase']


for i in range(0,9,1):
    print(" ")
    print(table.columns[i])
    collection = db[f'{table.columns[i]}']
    num = 0
    for j in range(0, table.count(axis='columns')[i], 1):
        print(table.iloc[j][i])
        post = {"CarreraID":i,"ClassID":num,"Mayor":table.columns[i],"class":table.iloc[j][i],}
        collection.insert_one(post)
        num = num+1


