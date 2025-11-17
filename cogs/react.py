from discord.ext import commands
import discord


class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def parse_emoji(emoji_str: str):
        """
        Converts unicode or <a:name:id> / <:name:id> into the proper format.
        Unicode -> stays string
        Custom emoji -> PartialEmoji
        """
        if emoji_str.startswith("<") and emoji_str.endswith(">"):
            try:
                return discord.PartialEmoji.from_str(emoji_str)
            except:
                pass
        return emoji_str  # unicode emoji

    @commands.command(name="react")
    async def react(self, ctx, message_id: int = None, *emojis):
        """
        React to a message in the CURRENT channel only.
        Usage: i!react message_id 😀 <:custom:123> <a:animated:456>
        """
        if message_id is None or not emojis:
            return await ctx.send(
                "❌ Usage: `i!react message_id emoji1 emoji2 ...`")

        # Try fetching the message in ANY channel
        try:
            # If the user provides a channel ID or mention
            channel_arg = ctx.message.content.split(
            )[1]  # assumes command: i!react <channel> <message_id> <emoji...>

            # Convert mention to ID if needed
            if channel_arg.startswith("<#") and channel_arg.endswith(">"):
                channel_id = int(channel_arg[2:-1])
            else:
                channel_id = int(channel_arg)

            # Fetch channel object
            channel = ctx.guild.get_channel(
                channel_id) or await ctx.guild.fetch_channel(channel_id)

            # Fetch message
            message_id = int(ctx.message.content.split()[2])
            message = await channel.fetch_message(message_id)

        except discord.NotFound:
            return await ctx.send("❌ Message or channel not found.")
        except discord.Forbidden:
            return await ctx.send("❌ I cannot access that channel or message.")
        except Exception as e:
            return await ctx.send(f"⚠️ Unexpected error: {e}")

        # Permission check
        if not ctx.channel.permissions_for(ctx.me).add_reactions:
            return await ctx.send(
                "❌ I don’t have permission to add reactions here.")

        failed = []

        for e in emojis:
            parsed = self.parse_emoji(e)
            try:
                await message.add_reaction(parsed)
            except Exception:
                failed.append(e)

        if failed:
            return await ctx.send(
                f"⚠️ These reactions failed: {', '.join(failed)}")

        await ctx.send(f"✅ Reacted to the message with: {', '.join(emojis)}")


async def setup(bot):
    await bot.add_cog(React(bot))
