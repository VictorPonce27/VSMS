import discord
import discord.emoji
from discord.ext import commands

import config
from config import token

import os

import pymongo
from pymongo import MongoClient

import pandas as pd

local_dir = os.getcwd()

clases = pd.read_csv(f'{local_dir}/ClasesFinalFINAL.csv')

print(clases)

client = commands.Bot(command_prefix='.')

cluster = MongoClient("mongodb+srv://victor:8246@cluster1.i5pf9.mongodb.net/Discrod?retryWrites=true & w=majority")

db = cluster["Data"]
collection = db["Users"]


# This gives you a message to let you know that the bot is on


@client.event
async def on_ready():
    print('Bot is ready.')
# This lets you know in the console when someone has joined


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    await member.send('hello tester')
    print(f'Bienvenido! Reacciona a este mensaje con el emoji que corresponde a tu carrera:')
    # print(f':rocket:')
    await member.send("""Bienvenido al servidor para apoyo de estudiantes
                         porfavor reacciona a los siguientes emojis 
                         dependiendo de tu carrera:
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

    print(payload.emoji.name)
    #Ambiente Construido
    if payload.emoji.name=='👷':
    print(payload.emoji.name)
    if payload.emoji.name=='⚒️':
        carrera=0
        
    #Ciencias Sociales
    elif payload.emoji.name=='📱':
    elif payload.emoji.name=='ciencias sociales':
        carrera=1

    #Estudios Creativos
    elif payload.emoji.name=='🎸':
    elif payload.emoji.name=='Estudios creativos':
        carrera=2

    #Negocios
    elif payload.emoji.name=='💸 ':
    elif payload.emoji.name=='negocios ':
        carrera=3

    #Salud
    elif payload.emoji.name=='🏥':
    elif payload.emoji.name=='salud':
        carrera=4

    #Inovación y Transformación
    elif payload.emoji.name=='🚀':
    elif payload.emoji.name=='innovacion y transformacion':
        carrera=5

    #Computación y Tecnología de Información
    elif payload.emoji.name=='💻':
    elif payload.emoji.name=='computacion y tecnologias de informacion':
        carrera=6

    #Bioingeniería y Procesos Químicos
    elif payload.emoji.name=='🧪':
    elif payload.emoji.name=='bioingenieria y procesos quimicos':
        carrera=7

    #Ciencias Aplicadas
    elif payload.emoji.name=='🔭':
    elif payload.emoji.name=='ciencias aplicadas':
        carrera=8

    #Send information to data base
    post = {"user": payload.user_id, "Carrera": carrera}
    collection.insert_one(post)

@client.command(name="command")
async def _command(ctx):
    global times_used
    await ctx.send(f"y or n")

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

    msg = await client.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("you said yes")
    else:
        await ctx.send("you said no")

    post = {"user": ctx.author.name, "answer": msg.content.lower()}
    collection.insert_one(post)

    times_used = times_used + 1


client.run(token)