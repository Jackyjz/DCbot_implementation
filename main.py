import discord
from discord.ext import commands
from apikeys import dcbottoken,channel_id
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("The bot is ready to operate")
    print("---------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am JZbot, a bot created by JZ")

@client.command()
async def goodbye(ctx):
    await ctx.send("See you next time!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(channel_id)  
    if channel:
        await channel.send(f"Hello {member.mention}! Welcome to the server!")


@client.event 
async def on_member_remove(member):
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(f"{member.mention} has left the server. Goodbye!")



client.run(dcbottoken)

