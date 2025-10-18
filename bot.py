# main.py
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive  # Only if using Replit

# -------------------------------
# 1️⃣ Bot token
# -------------------------------
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# -------------------------------
# 2️⃣ Intents
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True
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
        return  # Ignore messages from bots
    await bot.process_commands(message)

# -------------------------------
# 5️⃣ Load cogs (modular commands)
# -------------------------------
initial_extensions = [
    "cogs.ping",       # Example ping command
    "cogs.greetings"   # Future greetings cog
]

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

# -------------------------------
# 6️⃣ Keep alive (for Replit) and run bot
# -------------------------------
keep_alive()  # Optional, only if using Replit
bot.run(BOT_TOKEN)
