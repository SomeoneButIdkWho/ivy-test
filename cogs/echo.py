from discord.ext import commands

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, text):
        await ctx.send(text)

async def setup(bot):
    await bot.add_cog(Echo(bot))
