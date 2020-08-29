import discord
from discord.ext import commands
import config 
from config import token

client = commands.Bot(command_prefix = '.')







# This gives you a message to let you know that the bot is on
@client.event
async def on_ready():
    print('Bot is ready.')
# This lets you know in the console when someone has joined
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

# This lets you know in the console when someone has left
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

#comand for getting the info about the bot
@client.command()
async def info(ctx):
    await ctx.send(f'This is the Hackaton 2020 bot under going development {round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)


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
        await ctx.send("You said yes!")
    else:
        await ctx.send("You said no!")

    times_used = times_used + 1


client.run(token)