from discord.ext import commands
import discord
import re

# Your own max input limit. The bot will split messages automatically.
MAX_INPUT_LENGTH = 10000
DISCORD_MAX = 2000


class Echo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=(
        "Echo any message. Use a channel mention or name at the start to send there "
        "(e.g., i!echo #general message), or use normally to echo here."))
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def echo(self, ctx, *, text: str = None):

        # No DMs
        if ctx.guild is None:
            await ctx.send("❌ Echo cannot be used in DMs for safety.")
            return

        # Empty check
        if text is None or text.strip() == "":
            await ctx.send("❌ Cannot echo an empty message.")
            return

        # Silent flag
        silent = False
        if text.endswith('--silent') or text.endswith('-s'):
            text = text.rsplit('--silent', 1)[0].strip()
            text = text.rsplit('-s', 1)[0].strip()
            silent = True

        # Channel parsing (#general or <#id>)
        channel_match = re.match(r'(?:<#(\d+)>|#([\w-]+))\s*([\s\S]*)', text)
        target_channel = ctx.channel
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

        # 🔥 DO NOT TOUCH SPACING, DO NOT REMOVE ANYTHING
        # Only prevent mass pings
        safe_msg = (message.replace("@everyone", "@\u200b​everyone").replace(
            "@here", "@\u200b​here"))

        # Input limit
        if len(safe_msg) == 0:
            await ctx.send("❌ Cannot echo an empty message.")
            return

        if len(safe_msg) > MAX_INPUT_LENGTH:
            await ctx.send(
                f"❌ Message too large! ({len(safe_msg)}/{MAX_INPUT_LENGTH} characters)"
            )
            return

        # 🔥 EXACT RAW PASTE — PRESERVE ALL PARAGRAPHS
        # Split for Discord 2000-character limit only
        chunks = [
            safe_msg[i:i + DISCORD_MAX]
            for i in range(0, len(safe_msg), DISCORD_MAX)
        ]

        # Send chunks in order
        for chunk in chunks:
            await target_channel.send(chunk)

        # Delete original if echoed in same channel
        if target_channel == ctx.channel:
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass

        # Send confirmation if echoing elsewhere
        elif not silent:
            await ctx.send(f"✅ Echoed to {target_channel.mention}.")


async def setup(bot):
    await bot.add_cog(Echo(bot))
