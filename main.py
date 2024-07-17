import discord
from discord.ext import commands
from discord import app_commands
from apiandkeys import dcbottoken, channel_id

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Sync the command tree with the Discord server
        await self.tree.sync()

client = MyBot()

# Dictionary to store user IDs and their corresponding message IDs
user_messages = {}

@client.event
async def on_ready():
    print("The bot is ready to operate")
    print("---------------------------")

# Traditional command examples
@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am JZbot, a bot created by JZ")

@client.command()
async def goodbye(ctx):
    await ctx.send("See you next time!")

# Slash command examples
@client.tree.command(name="hello", description="Say hello")
async def slash_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! I am JZbot, a bot created by JZ")

@client.tree.command(name="goodbye", description="Say goodbye")
async def slash_goodbye(interaction: discord.Interaction):
    await interaction.response.send_message("See you next time!")

@client.tree.command(name="senddm", description="Send a DM to a user")
@app_commands.describe(username="The username of the person to send a DM to", message="The message to send")
async def slash_senddm(interaction: discord.Interaction, username: str, message: str):
    user = discord.utils.get(interaction.guild.members, name=username)
    if user:
        try:
            await user.send(message)
            await interaction.response.send_message(f"Message sent to {user.name}.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to send message to {user.name}. Error: {e}")
    else:
        await interaction.response.send_message(f"User {username} not found.")

@client.tree.command(name="anonymous", description="Send an anonymous message to the channel")
@app_commands.describe(message="The message to send anonymously")
async def slash_anonymous(interaction: discord.Interaction, message: str):
    channel = client.get_channel(channel_id)
    if channel:
        try:
            sent_message = await channel.send(f"Anonymous message: {message}")
            user_messages[interaction.user.id] = sent_message.id
            await interaction.response.send_message("Your anonymous message was sent successfully.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to send your anonymous message. Error: {e}", ephemeral=True)
    else:
        await interaction.response.send_message("Failed to send your message. The target channel was not found.", ephemeral=True)

@client.tree.command(name="undo", description="Undo your last anonymous message")
async def slash_undo(interaction: discord.Interaction):
    if interaction.user.id in user_messages:
        message_id = user_messages.pop(interaction.user.id)
        channel = client.get_channel(channel_id)
        if channel:
            try:
                message_to_delete = await channel.fetch_message(message_id)
                await message_to_delete.delete()
                await interaction.response.send_message("Your anonymous message was deleted successfully.", ephemeral=True)
            except discord.errors.Forbidden:
                await interaction.response.send_message("Failed to delete your message. The bot lacks the necessary permissions.", ephemeral=True)
            except discord.errors.NotFound:
                await interaction.response.send_message("Failed to delete your message. The message was not found.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Failed to delete your message. Error: {e}", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to delete your message. The target channel was not found.", ephemeral=True)
    else:
        await interaction.response.send_message("You have no message to undo.", ephemeral=True)

client.run(dcbottoken)
