from discord.ext import commands
import discord
import re

# Discord's max message length
MAX_MSG_LENGTH = 2000


class Echo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help=
        "Echo any message. Use a channel mention or name at the start to send there (e.g., i!echo #general hello!), or use normally to echo here."
    )
    @commands.cooldown(
        1, 3, commands.BucketType.user)  # 1 use per 3 seconds per user
    async def echo(self, ctx, *, text: str):
        """
        Echo a message; optionally specify a channel or use --silent to suppress feedback.
        Usage:
          i!echo some text
          i!echo #general hello!
          i!echo <#123456789012345678> hello!
          i!echo #general --silent secret text
        """
        # Prevent use in DMs:
        if ctx.guild is None:
            await ctx.send("❌ Echo cannot be used in DMs for safety.")
            return

        # Silent mode
        silent = False
        if text.endswith('--silent') or text.endswith('-s'):
            text = text.rsplit('--silent', 1)[0].strip()
            text = text.rsplit('-s', 1)[0].strip()
            silent = True

        # Channel parsing: mention or #name
        channel_match = re.match(r'(?:<#(\d+)>|#([\w-]+))\s*(.*)', text)
        target_channel = ctx.channel  # default
        message = text

        if channel_match:
            channel_id = channel_match.group(1)
            channel_name = channel_match.group(2)
            message = channel_match.group(3)
            channel = None
            if channel_id:
                channel = ctx.guild.get_channel(int(channel_id))
            elif channel_name:
                channel = discord.utils.get(ctx.guild.text_channels,
                                            name=channel_name)
            if channel:
                target_channel = channel

        # Sanitize, limit message length, prevent mass mentions
        safe_msg = message.replace("@everyone", "@\u200beveryone").replace(
            "@here", "@\u200bhere")
        safe_msg = safe_msg.strip()
        if len(safe_msg) > MAX_MSG_LENGTH:
            await ctx.send(
                f"❌ Message too long! ({len(safe_msg)}/2000 characters)")
            return
        if len(safe_msg) == 0:
            await ctx.send("❌ Cannot echo an empty message.")
            return

        # Send message
        await target_channel.send(safe_msg)
        if not silent:
            if target_channel != ctx.channel:
                await ctx.send(f"✅ Echoed to {target_channel.mention}.")
            else:
                await ctx.message.delete()
                await target_channel.send(f"✅ Echoed successfully!")


# Setup function, unchanged
async def setup(bot):
    await bot.add_cog(Echo(bot))
