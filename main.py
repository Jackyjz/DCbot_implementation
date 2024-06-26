import discord
from discord.ext import commands
from apikeys import dcbottoken

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Add this line

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
    channel = client.get_channel(1091095815851876468)  # Use the ID of the channel you want to send the message to
    if channel:
        await channel.send(f"Hello {member.mention}! Welcome to the server!")

client.run(dcbottoken)
