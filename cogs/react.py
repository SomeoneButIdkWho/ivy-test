from discord.ext import commands
import discord


class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Utility: Converts Unicode/custom/animated emoji into a usable format
    @staticmethod
    def parse_emoji(emoji_str: str):
        """
        Converts raw emoji input into a PartialEmoji if possible.
        Ensures compatibility with Unicode, static, and animated custom emojis.
        """
        try:
            # Handles custom: <:name:id>  or  <a:name:id>
            if emoji_str.startswith("<") and emoji_str.endswith(">"):
                return discord.PartialEmoji.from_str(emoji_str)
        except Exception:
            pass

        # Otherwise Unicode emoji stays a plain string
        return emoji_str

    @commands.command(
        help=
        "React to a message with one or more emojis.\nUsage: i!react message_id 😀 🎉 👍 <:custom:123> <a:animated:456>"
    )
    async def react(self, ctx, message_id: int = None, *emojis):
        """
        Reacts to a message with all given emojis (Unicode, custom, animated).
        Usage: i!react message_id 😀 🎉 👍 <:smile:123> <a:dance:456>
        """
        if message_id is None or not emojis:
            await ctx.send("❌ Usage:\n`i!react message_id 😀 🎉 👍`")
            return

        target_message = None
        target_channel = None

        # Try fetching in current channel first
        try:
            target_message = await ctx.channel.fetch_message(message_id)
            target_channel = ctx.channel
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        # If not found, search all text channels
        if not target_message and ctx.guild:
            for channel in ctx.guild.text_channels:
                perms = channel.permissions_for(ctx.me)
                if not perms.read_messages:
                    continue
                try:
                    msg = await channel.fetch_message(message_id)
                    target_message = msg
                    target_channel = channel
                    break
                except (discord.NotFound, discord.Forbidden,
                        discord.HTTPException):
                    continue

        if not target_message or not target_channel:
            await ctx.send(
                "❌ Message not found. Ensure the message ID is valid and accessible."
            )
            return

        # Check permissions
        if not target_channel.permissions_for(ctx.me).add_reactions:
            await ctx.send(
                "❌ I don't have permission to add reactions in that channel.")
            return

        errors = []

        for raw_emoji in emojis:
            parsed_emoji = self.parse_emoji(raw_emoji)

            try:
                await target_message.add_reaction(parsed_emoji)
            except discord.Forbidden:
                errors.append(f"{raw_emoji} (forbidden)")
            except discord.HTTPException as e:
                errors.append(f"{raw_emoji} (HTTP error: {e})")
            except Exception as e:
                errors.append(f"{raw_emoji} ({type(e).__name__})")

        if errors:
            await ctx.send(f"⚠️ Some reactions failed: {', '.join(errors)}")
        else:
            await ctx.send(
                f"✅ Added reactions {', '.join(emojis)} to [this message]({target_message.jump_url}) in {target_channel.mention}!"
            )


async def setup(bot):
    await bot.add_cog(React(bot))
