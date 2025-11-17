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
        if isinstance(
                emoji_str,
                str) and emoji_str.startswith("<") and emoji_str.endswith(">"):
            try:
                return discord.PartialEmoji.from_str(emoji_str)
            except Exception:
                pass
        return emoji_str  # Unicode emoji

    @commands.command(
        name="react",
        help=
        "React to a message in this channel. Usage: i!react <message_id> <emoji> [emoji...]"
    )
    async def react(self, ctx, message_id: int = None, *emojis):
        """
        React to a message in the current channel only.
        Usage: i!react <message_id> 😀 <:custom:123> <a:animated:456>
        """
        if message_id is None or not emojis:
            await ctx.send("❌ Usage: `i!react <message_id> emoji1 emoji2 ...`")
            return

        # Try fetching the message in the current channel
        try:
            message = await ctx.channel.fetch_message(int(message_id))
        except discord.NotFound:
            await ctx.send("❌ Message not found.")
            return
        except (discord.Forbidden, AttributeError):
            await ctx.send("❌ I cannot access that message.")
            return
        except Exception as e:
            await ctx.send(f"⚠️ Unexpected error: `{e}`")
            return

        # Permission check for add_reactions in THIS channel
        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.add_reactions:
            await ctx.send("❌ I don’t have permission to add reactions here.")
            return

        failed = []

        for e in emojis:
            parsed = self.parse_emoji(e)
            try:
                await message.add_reaction(parsed)
            except Exception:
                failed.append(e)

        if failed:
            await ctx.send(f"⚠️ Could not react with: {', '.join(failed)}")
        else:
            await ctx.send(
                f"✅ Reacted to the message with: {', '.join(emojis)}")


async def setup(bot):
    await bot.add_cog(React(bot))
