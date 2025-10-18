from discord.ext import commands
import discord
import re


class Echo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, text):
        """
        Echo a message. Optionally specify a channel:
        i!echo #channel-name message
        """
        # Regex to check for a channel mention at the start of the text
        match = re.match(r'<#(\d+)>\s*(.*)', text)
        if match:
            channel_id = int(match.group(1))
            message = match.group(2)
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                await channel.send(message)
                await ctx.send(f"✅ Message sent to {channel.mention}")
            else:
                await ctx.send("❌ Could not find that channel.")
        else:
            # No channel mentioned, send in the current channel
            await ctx.send(text)


async def setup(bot):
    await bot.add_cog(Echo(bot))
