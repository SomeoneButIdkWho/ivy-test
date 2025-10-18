from discord.ext import commands
import discord

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, channel: discord.TextChannel = None, reply: bool = False, *, text):
        """
        Echo a message to a specified channel, optionally replying to the user.
        Usage:
        !echo #channel your message
        !echo True your message  -> replies in current channel
        !echo #channel True your message -> replies in specified channel
        """
        target_channel = channel or ctx.channel  # default to current channel

        if reply:
            await target_channel.send(text, reference=ctx.message)
        else:
            await target_channel.send(text)

        if channel:
            await ctx.send(f"✅ Message sent to {channel.mention}")

async def setup(bot):
    await bot.add_cog(Echo(bot))

