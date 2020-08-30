from pymongo import MongoClient, errors
import pymongo
from pymongo import MongoClient

import os

# import pandas
# import pandas as pd

cluster = pymongo.MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")


db1 = cluster['MajorsDatabase']

dbu = cluster['UserData']
collectionu = dbu['data']

df = ["Ambiente Construido", "Ciencias Sociales",
      "Estudios Creativos", "Negocios", "Salud", "Innovacion y transformacion", 
      "Computacion y Tecnologias de Informacion", "Bioingenieria y Procesos Quimicos",
      "Ciencias aplicadas"]

"""
database_names() AND collection_names ARE DEPRECATED
"""
# collection = db["Ambiente Construido"]
database_names = cluster.list_database_names()

# iterate over the list of database names
for db_num, db in enumerate(database_names):
    # use the list_collection_names() method to return collection names
    collection_names = cluster[db].list_collection_names()
    if(db == "MajorsDatabase"):
        # iterate over the list of collection names
        for col in df:
            print(col, "--")
            collection = db1[col]
            myquery = {"major":col}
            mydoc = collection.find(myquery)
            aux= []
            count = 0
            for i in mydoc: 
                myquery2 = {"major":i["major"]}
                mydoc2 = collectionu.find(myquery2)
                for j in mydoc2:
                    print({'classID': i['classID']})
                    if(i["classID"] == j["class"]):
                        print("inside")
                        print({'class':i['class']})
                        print(" ")
                        print({'class':j['class']})
                        aux.append(j['username'])
                        count = count + 1 
                print(len(aux))
                if(len(aux) == 5):
                    print(aux)



