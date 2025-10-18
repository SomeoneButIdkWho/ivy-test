from discord.ext import commands
import random

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greetings = ['Hello!', 'Hi there!', 'Hey!', 'Yo!']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if any(word in message.content.lower() for word in ['hi', 'hello', 'hey']):
            await message.channel.send(random.choice(self.greetings))

async def setup(bot):
    await bot.add_cog(Greetings(bot))
