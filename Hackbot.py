import discord
import discord.emoji
from discord.ext import commands, tasks

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

@client.loop(seconds = 60.0)
async def matching():
    print("place holder")    


@client.command(name="study")
async def study(ctx, arg):
    collectionu = dbu["data"]

    index = int(arg)

    myquery = {"class": ctx.message.author.id}
    newData = {"$set": {"class": index - 1}}
    collectionu.update_one(myquery, newData)

    await ctx.send("Thanks! Hang tight, we're finding the best matches for you. This might take around a minute.")

client.run(token)
