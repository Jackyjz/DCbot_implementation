import discord
from discord.ext import commands
from apiandkeys import dcbottoken, channel_id

#Bot Set Up with necessary Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

# Create bot instance with command prefix '!'
client = commands.Bot(command_prefix='!', intents=intents)

#will say ready in the termina if the code is sucessfully compiled
@client.event
async def on_ready():
    print("The bot is ready to operate")
    print("---------------------------")

#command to greet users
@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am JZbot, a bot created by JZ")

#command to say goodbye to users
@client.command()
async def goodbye(ctx):
    await ctx.send("See you next time!")

#Bot greeting users when they join the server
@client.event
async def on_member_join(member):
    print(f"on_member_join event triggered for {member}")
    channel = client.get_channel(channel_id)  
    if channel:
        await channel.send(f"Hello {member.mention}! Welcome to the server!")

#Bot saying goodbye to users when they leave the server
@client.event 
async def on_member_remove(member):
    print(f"on_member_remove event triggered for {member}")
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(f"{member.mention} has left the server. Goodbye!")

#command that sends a DM to a user
@client.command()
# Look for the user in the server by their username
async def senddm(ctx, username: str, *, message: str):
    user = discord.utils.get(ctx.guild.members, name=username)
    if user:
        try:
             # Attempt to send the direct message to the user
            await user.send(message)
             # Inform the command issuer that the message was sent successfully
            await ctx.send(f"Message sent to {user.name}.")
        except Exception as e:
            # Inform the command issuer that there was an error sending the message
            await ctx.send(f"Failed to send message to {user.name}. Error: {e}")
    else:
           # Inform the command issuer that the user was not found
        await ctx.send(f"User {username} not found.")


#event to send anonymous messages (triggers when a message is received)
@client.event
async def on_message(message):
    # Check if the message is a DM and not sent by a bot
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        # Log the message details for debugging
        print(f"Message from {message.author}: {message.content}")

        # Get the channel object where messages will be forwarded
        channel = client.get_channel(channel_id)
        if channel:
            try:
                # Use for Debugging -> Indicate that the message forwarding is triggered
                print("it's triggered")
                # Send the anonymous message to the specified channel
                await channel.send(f"Anonymous message: {message.content}")
                # Inform the user that their message was sent successfully
                await message.author.send("Your message was sent successfully.")
            except Exception as e:
                # Inform the user that there was an error sending their message
                await message.author.send(f"Failed to send your message. Error: {e}")
        else:
            # Inform the user that the specified channel was not found
            await message.author.send("Failed to send your message. The target channel was not found.")
    # Ensure the bot processes other commands
    await client.process_commands(message)


# Run the bot with the provided token
client.run(dcbottoken)
