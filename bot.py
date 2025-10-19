import discord
from discord.ext import commands, tasks
import os
import asyncio
from keep_alive import keep_alive

BOT_TOKEN = os.environ['BOT_TOKEN']

# -----------------------------
# Setup Intents & Bot
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="i!", intents=intents)

# -----------------------------
# Rotating Status List
# -----------------------------
statuses = [
    discord.Game(name="i!help"),
    discord.Activity(type=discord.ActivityType.listening,
                     name="your commands"),
    discord.Activity(type=discord.ActivityType.watching,
                     name="over Ivy’s server"),
    discord.Activity(type=discord.ActivityType.competing,
                     name="in bot olympics")
]


# -----------------------------
# Load Cogs
# -----------------------------
async def load_cogs():
    cogs_folder = "./cogs"
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load cog {cog_name}: {e}")


# -----------------------------
# Status Rotation Task
# -----------------------------
@tasks.loop(seconds=120)  # change every 2 minutes
async def change_status():
    for status in statuses:
        await bot.change_presence(activity=status)
        await asyncio.sleep(120)


# -----------------------------
# On Ready Event
# -----------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not change_status.is_running():
        change_status.start()


# -----------------------------
# Main Entry
# -----------------------------
async def main():
    async with bot:
        await load_cogs()
        keep_alive()
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
