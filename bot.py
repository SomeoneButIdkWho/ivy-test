import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# -------------------------------
# 1️⃣ Put your bot token here
# -------------------------------
import os
BOT_TOKEN = os.environ['BOT_TOKEN'] # <-- Replace this

# -------------------------------
# 2️⃣ Set up intents & bot
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------
# 3️⃣ Load all cogs from cogs/
# -------------------------------
cogs_folder = "./cogs"

for filename in os.listdir(cogs_folder):
    if filename.endswith(".py"):
        cog_name = filename[:-3]  # Remove .py
        try:
            bot.load_extension(f"cogs.{cog_name}")
            print(f"Loaded cog: {cog_name}")
        except Exception as e:
            print(f"Failed to load cog {cog_name}: {e}")

# -------------------------------
# 4️⃣ Bot events
# -------------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# -------------------------------
# 5️⃣ Keep the bot alive (Flask)
# -------------------------------
keep_alive()

# -------------------------------
# 6️⃣ Run the bot
# -------------------------------
bot.run(BOT_TOKEN)
