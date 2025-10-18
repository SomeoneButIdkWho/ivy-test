from discord.ext import commands

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx, *, text):
        await ctx.reply(text)

def setup(bot):
    bot.add_cog(Reply(bot))
