from discord.ext import commands
import datetime

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # ms
        uptime = datetime.datetime.utcnow() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"🏓 Pong!\nLatency: `{latency}ms`\nUptime: `{hours}h {minutes}m {seconds}s`")

async def setup(bot):
    await bot.add_cog(Ping(bot))
