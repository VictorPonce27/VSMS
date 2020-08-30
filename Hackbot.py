import discord
import discord.emoji
from discord.ext import tasks, commands

from itertools import cycle 

import config
from config import token

import os

import pymongo
from pymongo import MongoClient

import pandas as pd


client = commands.Bot(command_prefix='.')

cluster = pymongo.MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")

db = cluster["MajorsDatabase"]
dbu = cluster["UserData"]

# This gives you a message to let you know that the bot is on


@client.event
async def on_ready():
    print('Bot is ready.')
    db1 = cluster['MajorsDatabase']

    dbu = cluster['UserData']
    collectionu = dbu['data']

    df = ["Ambiente Construido", "Ciencias Sociales",
          "Estudios Creativos", "Negocios", "Salud", "Innovacion y transformacion",
          "Computacion y Tecnologias de Informacion", "Bioingenieria y Procesos Quimicos",
          "Ciencias aplicadas"]

    database_names = cluster.list_database_names()

    # iterate over the list of database names
    for db_num, db in enumerate(database_names):
        # use the list_collection_names() method to return collection names
        collection_names = cluster[db].list_collection_names()
        if(db == "MajorsDatabase"):
            # iterate over the list of collection names
            for col in df:
                # print(col, "--")
                collection = db1[col]
                myquery = {"major": col}
                mydoc = collection.find(myquery)
                aux = []
                auxid = []
                count = 0
                for i in mydoc:
                    myquery2 = {"major": i["major"]}
                    mydoc2 = collectionu.find(myquery2)
                    for j in mydoc2:

                        if(i["classID"] == j["class"]):
                            aux.append(j['username'])
                            auxid.append(j['user_id'])
                            count = count + 1
                   
                    if (len(aux) >= 3):
                        for i in range(0, len(aux)):
                            await client.get_user(auxid[i]).send("Gracias por la espera! Tu equipo es...")
                        for j in range(0, len(aux)):
                            await client.get_user(auxid[i]).send(f"{j}: {aux[j]}")
                        await client.get_user(auxid[i]).send("Favor de comunicarte con ellos via discord. :D")

                        mydb = cluster['UserData']
                        mycollection = mydb['data']
                        for i in range(0, len(aux)):
                            myquery = {"username": aux[i]}
                            mycollection.delete_one(myquery)
                        aux.clear()
# This lets you know in the console when someone has joined


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    print(f'Bienvenido! Reacciona a este mensaje con el emoji que corresponde a tu carrera:')
    # print(f':rocket:')
    await member.send("""Bienvenido al Valgrind Study Group Matching Service!
                         Reacciona a este mensaje con uno de los siguientes emojis dependiendo de tu area de estudio:
                         
                         👷 para ambiente construido
                         📱 para ciencias sociales
                         🎸 para estudios creativos
                         💸 para negocios
                         🏨 para salud 
                         🚀 para innovacion y transformacion
                         💻 para computacion y tecnologias de informacion
                         🧪 para bioigenieria y procesos quimicos
                         🔭 para ciencias aplicadas""")


# This lets you know in the console when someone has left

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

#comand for getting the info about the bot

@client.command()
async def info(ctx):
    await ctx.send(f'This bot helps you math with other students that are trying to study the same thing as you {round(client.latency * 1000)}ms')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#comand for creating reaction
@client.event
async def on_raw_reaction_add(payload):

    print(client.get_user(payload.user_id) )
    user = client.get_user(payload.user_id) 

    carrera = 100
    carreraID =100
    #Ambiente Construido
    if payload.emoji.name=='👷':
        carrera = "Ambiente Construido"
        carreraID = 0
    #Ciencias Sociales
    elif payload.emoji.name=='📱':
        carrera = "Ciencias Sociales"
        carreraID = 1
    #Estudios Creativos
    elif payload.emoji.name=='🎸':
        carrera = "Estudios Creativos"
        carreraID = 2
    #Negocios
    elif payload.emoji.name=='💸':
        carrera = "Negocios"
        carreraID = 3
    #Salud
    elif payload.emoji.name=='🏥':
        carrera = "Salud"
        carreraID = 4
    #Inovación y Transformación
    elif payload.emoji.name=='🚀':
        carrera = "Innovacion y transformacion"
        carreraID = 5
    #Computación y Tecnología de Información
    elif payload.emoji.name=='💻':
        carrera = "Computacion y Tecnologias de Informacion"
        carreraID = 6
    #Bioingeniería y Procesos Químicos
    elif payload.emoji.name=='🧪':
        carrera = "Bioingenieria y Procesos Quimicos"
        carreraID = 7
    #Ciencias Aplicadas
    elif payload.emoji.name=='🔭':
        carrera = "Ciencias aplicadas"
        carreraID = 8
    collection1 = db[carrera]

    myquery = {"majorID":carreraID}
    mydoc = collection1.find(myquery)
    number = 1

    for i in mydoc:
        print(i['class'])
        await user.send(f"{number}: {i['class']}")   
        number = number + 1 
    
    await user.send("reply with .study(number of the class wich you want to study)")

    collectionu = dbu["data"]
    post = {"user_id": user.id, "username" : user.name, "major":carrera, "class":""}
    collectionu.insert_one(post)


@client.command(name="study")
async def study(ctx, arg):
    collectionu = dbu["data"]

    index = int(arg)

    myquery = {"class": ctx.message.author.id}
    newData = {"$set": {"class": index - 1}}
    collectionu.update_one(myquery, newData)

    await ctx.send("Thanks! Hang tight, we're finding the best matches for you. This might take around a minute.")

# @tasks.loop(seconds = 3.0)
# async def matching():
#     db1 = cluster['MajorsDatabase']

#     dbu = cluster['UserData']
#     collectionu = dbu['data']

#     df = ["Ambiente Construido", "Ciencias Sociales",
#           "Estudios Creativos", "Negocios", "Salud", "Innovacion y transformacion",
#           "Computacion y Tecnologias de Informacion", "Bioingenieria y Procesos Quimicos",
#           "Ciencias aplicadas"]

#     database_names = cluster.list_database_names()

#     # iterate over the list of database names
#     for db_num, db in enumerate(database_names):
#         # use the list_collection_names() method to return collection names
#         collection_names = cluster[db].list_collection_names()
#         if(db == "MajorsDatabase"):
#             # iterate over the list of collection names
#             for col in df:
#                 print(col, "--")
#                 collection = db1[col]
#                 myquery = {"major": col}
#                 mydoc = collection.find(myquery)
#                 aux = []
#                 count = 0
#                 for i in mydoc:
#                     myquery2 = {"major": i["major"]}
#                     mydoc2 = collectionu.find(myquery2)
#                     for j in mydoc2:
#                         print({'classID': i['classID']})
#                         if(i["classID"] == j["class"]):
#                             print("inside")
#                             print({'class': i['class']})
#                             print(" ")
#                             print({'class': j['class']})
#                             aux.append(j['username'])
#                             count = count + 1

#         print("Done")
#         if (len(aux) >= 3):
#             for i in range(0,len(aux)):
#                 await aux[i].send("Gracias por la espera! Tu equipo es...")
#             for j in range(0,len(aux)):
#                 await aux[i].send(f"{j}: {aux[j]}")
#             await aux[i].send("Favor de comunicarte con ellos via discord. :D")

#         mydb = cluster['UserData']
#         mycollection = mydb['data']
#         for i in range(0,len(aux)):
#             myquery = {"username" : aux[i]}
#             mycollection.delete_one(myquery)
#         aux.clear()
   

client.run(token)
