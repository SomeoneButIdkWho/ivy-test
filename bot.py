import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

BOT_TOKEN = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="i!", intents=intents)

# Load cogs
async def load_cogs():
    cogs_folder = "./cogs"
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

# Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# Main
async def main():
    keep_alive()           # keep bot alive
    await load_cogs()      # load all cogs
    await bot.start(BOT_TOKEN)  # start bot normally

if __name__ == "__main__":
    asyncio.run(main())
