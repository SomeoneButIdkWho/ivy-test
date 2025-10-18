import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

# -------------------------------
# 1️⃣ Put your bot token here
# -------------------------------
BOT_TOKEN = os.environ['BOT_TOKEN']

# -------------------------------
# 2️⃣ Set up intents & bot
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages
bot = commands.Bot(command_prefix="i!", intents=intents)


# -------------------------------
# 3️⃣ Load all cogs from cogs/
# -------------------------------
async def load_cogs():
    cogs_folder = "./cogs"
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py"):
            cog_name = filename[:-3]  # Remove .py
            try:
                await bot.load_extension(f"cogs.{cog_name}")
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
# 5️⃣ Main function
# -------------------------------
async def main():
    async with bot:
        await load_cogs()
        keep_alive()
        await bot.start(BOT_TOKEN)
        await bot.load_extension("cogs.ping")


# -------------------------------
# 6️⃣ Run the bot
# -------------------------------
if __name__ == "__main__":
    asyncio.run(main())
