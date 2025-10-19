from discord.ext import commands
import discord
import re

MAX_MSG_LENGTH = 2000


class Echo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help=
        "Echo any message. Use a channel mention or name at the start to send there (e.g., i!echo #general hello!), or use normally to echo here."
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def echo(self, ctx, *, text: str = None):
        """
        Echo a message; optionally specify a channel or use --silent.
        Usage:
          i!echo some text
          i!echo #general hello!
        """
        if ctx.guild is None:
            await ctx.send("❌ Echo cannot be used in DMs for safety.")
            return

        if text is None or text.strip() == "":
            await ctx.send("❌ Cannot echo an empty message.")
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

        # Check again if message is empty after channel parsing
        safe_msg = message.replace("@everyone", "@\u200beveryone").replace(
            "@here", "@\u200bhere").strip()
        if len(safe_msg) > MAX_MSG_LENGTH:
            await ctx.send(
                f"❌ Message too long! ({len(safe_msg)}/2000 characters)")
            return
        if len(safe_msg) == 0:
            await ctx.send("❌ Cannot echo an empty message.")
            return

        await target_channel.send(safe_msg)
        if not silent and target_channel != ctx.channel:
            await ctx.send(f"✅ Echoed to {target_channel.mention}.")


async def setup(bot):
    await bot.add_cog(Echo(bot))
