from discord.ext import commands
import discord


class Possess(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.possessed_user = None
        self.possessed_channel = None

    @commands.command()
    async def possess(self, ctx, user: discord.Member, channel_id: int = None):
        """Start echoing a user's messages."""
        self.possessed_user = user
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                await ctx.send("❌ Invalid channel ID provided!")
                return
            self.possessed_channel = channel
        else:
            self.possessed_channel = ctx.channel

        await ctx.send(
            f"👻 Now possessing {user.mention} in {self.possessed_channel.mention}."
        )

    @commands.command()
    async def unpossess(self, ctx):
        """Stop echoing the possessed user's messages."""
        if self.possessed_user is None:
            await ctx.send("ℹ️ No user is currently possessed.")
            return

        await ctx.send(f"✅ Stopped possessing {self.possessed_user.mention}.")
        self.possessed_user = None
        self.possessed_channel = None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot/bot-echoed messages
        if message.author.bot:
            return

        if (self.possessed_user and message.author.id == self.possessed_user.id
                and self.possessed_channel):
            # If echoing in the same channel, attempt to delete original message safely
            if message.channel == self.possessed_channel:
                try:
                    await message.delete()
                except discord.Forbidden:
                    # Can't delete, ignore
                    pass
                except discord.HTTPException:
                    # Message too old or another error
                    pass
            # Echo user's message content to target channel
            await self.possessed_channel.send(message.content)


async def setup(bot):
    await bot.add_cog(Possess(bot))
