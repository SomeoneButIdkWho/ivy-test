# main.py
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive  # Only if you're using Replit or similar

# -------------------------------
# 1️⃣ Bot token
# -------------------------------
BOT_TOKEN = os.environ.get(
    'BOT_TOKEN')  # Make sure your environment variable is set

# -------------------------------
# 2️⃣ Intents
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
intents.guilds = True
intents.members = True

# -------------------------------
# 3️⃣ Bot setup
# -------------------------------
bot = commands.Bot(command_prefix="i!", intents=intents)


# -------------------------------
# 4️⃣ Events
# -------------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# Prevent bot from replying to itself
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots including itself

    await bot.process_commands(message)  # Allow commands to be processed


# -------------------------------
# 5️⃣ Commands
# -------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# -------------------------------
# 6️⃣ Keep alive (for Replit) and run bot
# -------------------------------
keep_alive()  # Optional, only if using Replit
bot.run(BOT_TOKEN)
