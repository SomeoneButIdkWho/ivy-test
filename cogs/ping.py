from discord.ext import commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # convert to ms
        await ctx.send(f"Pong! 🏓 `{latency}ms`")

# setup function
async def setup(bot):
    await bot.add_cog(Ping(bot))
