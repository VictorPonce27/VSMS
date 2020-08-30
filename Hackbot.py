import discord
import discord.emoji
from discord.ext import commands, tasks

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
    await ctx.send(f'This is the Hackaton 2020 bot under going development {round(client.latency * 1000)}ms')


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
    elif payload.emoji.name=='💸 ':
        carrera = "Negocios"
        carreraID = 3
    #Salud
    elif payload.emoji.name=='🏥':
        carrera = "Salud"
        carreraID = 4
    #Inovación y Transformación
    elif payload.emoji.name=='🚀':
        carrera = "Innovacion y Transformacion"
        carreraID = 5
    #Computación y Tecnología de Información
    elif payload.emoji.name=='💻':
        carrera = "Computacion y Tecnologias de Informacion"
        carreraID = 6
    #Bioingeniería y Procesos Químicos
    elif payload.emoji.name=='🧪':
        carrera = "Bioigenieria y Procesos Quimicos"
        carreraID = 7
    #Ciencias Aplicadas
    elif payload.emoji.name=='🔭':
        carrera = "Ciencias Aplicadas"
        carreraID = 8
    collection = db[carrera]

    myquery = {"carreraID":carreraID}
    mydoc = collection.find(myquery)
    number = 1
    for i in mydoc:
        print(i['class'])
        await user.send(f"{number}: {i['class']}")   
        number = number + 1 
    await user.send("reply with .study(number of the class wich you want to study)")

    collectionu = dbu["data"]
    post = {"user": user.name, "major":carrera}
    collectionu.insert_one(post)

@task.loop(seconds = 60.0)
async def group(self):

    dbU = cluster['Data']
    collection = dbU['Users']





@client.command(name="command")
async def _command(ctx):
    global times_used
    await ctx.send(f"y or n")


@client.command(name="study")
async def _command(ctx):
    collectionu = dbu["data"]
    
    newData = {"$set":{"class":ctx}}
    collectionu.insert_one(newData)

    await ctx.send("Thanks. Hang tight we're finding the best matches for you")

client.run(token)
