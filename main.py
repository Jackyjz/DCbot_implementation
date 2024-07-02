import discord
from discord.ext import commands
from apiandkeys import dcbottoken, channel_id

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

client = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store user IDs and their corresponding message IDs
user_messages = {}

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
    print(f"on_member_join event triggered for {member}")
    channel = client.get_channel(channel_id)  
    if channel:
        await channel.send(f"Hello {member.mention}! Welcome to the server!")

@client.event 
async def on_member_remove(member):
    print(f"on_member_remove event triggered for {member}")
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(f"{member.mention} has left the server. Goodbye!")

@client.event
async def on_message(message):
    # Check if the message is a DM and not sent by a bot
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        # Check if the message is a command
        if message.content.startswith('!'):
            # Process the command
            await client.process_commands(message)
        else:
            # Log the message details for debugging
            print(f"Message from {message.author}: {message.content}")

            # Get the channel object where messages will be forwarded
            channel = client.get_channel(channel_id)
            if channel:
                try:
                    # Debugging: Indicate that the message forwarding is triggered
                    print("it's triggered")
                    # Send the anonymous message to the specified channel
                    sent_message = await channel.send(f"Anonymous message: {message.content}")
                    # Store the message ID with the user's ID
                    user_messages[message.author.id] = sent_message.id
                    # Log the message ID
                    print(f"Stored message ID {sent_message.id} for user {message.author.id}")
                    # Inform the user that their message was sent successfully
                    await message.author.send("Your message was sent successfully.")
                except Exception as e:
                    # Inform the user that there was an error sending their message
                    await message.author.send(f"Failed to send your message. Error: {e}")
            else:
                # Inform the user that the specified channel was not found
                await message.author.send("Failed to send your message. The target channel was not found.")
    else:
        # Ensure the bot processes other commands
        await client.process_commands(message)

@client.command()
async def undo(ctx):
    # Check if the user has sent a message to be undone
    if ctx.author.id in user_messages:
        # Get the message ID from the stored dictionary
        message_id = user_messages.pop(ctx.author.id)
        # Get the channel object where messages were forwarded
        channel = client.get_channel(channel_id)
        if channel:
            try:
                # Fetch the message by its ID and delete it
                print(f"Attempting to delete message ID {message_id} in channel ID {channel_id}")
                message_to_delete = await channel.fetch_message(message_id)
                print(f"Fetched message: {message_to_delete.content}")
                await message_to_delete.delete()
                print("Message deleted")
                # Inform the user that their message was deleted successfully
                await ctx.author.send("Your message was deleted successfully.")
            except discord.errors.Forbidden:
                print("The bot lacks the permissions to delete the message.")
                await ctx.author.send("Failed to delete your message. The bot lacks the necessary permissions.")
            except discord.errors.NotFound:
                print("The message to delete was not found.")
                await ctx.author.send("Failed to delete your message. The message was not found.")
            except Exception as e:
                # Inform the user that there was an error deleting their message
                print(f"Error deleting message: {e}")
                await ctx.author.send(f"Failed to delete your message. Error: {e}")
        else:
            # Inform the user that the specified channel was not found
            print("Channel not found")
            await ctx.author.send("Failed to delete your message. The target channel was not found.")
    else:
        # Inform the user that there is no message to undo
        print("No message to undo for this user")
        await ctx.author.send("You have no message to undo.")

client.run(dcbottoken)
