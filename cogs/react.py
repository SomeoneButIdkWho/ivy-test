from discord.ext import commands
import discord
from typing import Optional, Tuple


class Reacts(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def parse_emoji(emoji_str: str):
        """
        Convert raw input to PartialEmoji for custom/animated emojis,
        or keep unicode emoji as string.
        """
        # Allow already-resolved Emoji objects
        if not isinstance(emoji_str, str):
            return emoji_str
        try:
            if emoji_str.startswith("<") and emoji_str.endswith(">"):
                return discord.PartialEmoji.from_str(emoji_str)
        except Exception:
            # fallback to raw string
            pass
        return emoji_str

    async def _find_message(
        self, ctx: commands.Context, message_id: int
    ) -> Tuple[Optional[discord.Message], Optional[discord.TextChannel]]:
        """
        Tries to fetch the message in the current channel first, then scans
        accessible text channels in the guild.
        Returns (message, channel) or (None, None).
        """
        # Try current channel
        try:
            msg = await ctx.channel.fetch_message(message_id)
            return msg, ctx.channel
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        # If not found, and we're in a guild, try other text channels
        if ctx.guild:
            for channel in ctx.guild.text_channels:
                perms = channel.permissions_for(ctx.guild.me)
                if not perms.read_messages:
                    continue
                try:
                    msg = await channel.fetch_message(message_id)
                    return msg, channel
                except (discord.NotFound, discord.Forbidden,
                        discord.HTTPException):
                    continue
        return None, None

    def _bot_member_for_channel(
            self,
            channel: discord.abc.GuildChannel) -> Optional[discord.Member]:
        """Get the bot's Member object for permission checks, if possible."""
        if hasattr(channel, "guild") and channel.guild:
            return channel.guild.get_member(self.bot.user.id)
        return None

    @commands.command(
        name="react",
        help=("React to a message with one or more emojis.\n"
              "Usage: i!react message_id 😀 🎉 👍 <:custom:123> <a:anim:456>"))
    async def react(self,
                    ctx: commands.Context,
                    message_id: int = None,
                    *emojis):
        if message_id is None or not emojis:
            await ctx.send("❌ Usage:\n`i!react message_id 😀 🎉 👍`")
            return

        target_message, target_channel = await self._find_message(
            ctx, message_id)
        if not target_message or not target_channel:
            await ctx.send(
                "❌ Message not found. Ensure the message ID is valid and accessible."
            )
            return

        bot_member = self._bot_member_for_channel(target_channel)
        perms = target_channel.permissions_for(bot_member or ctx.me)
        if not perms.add_reactions:
            await ctx.send(
                "❌ I don't have permission to add reactions in that channel.")
            return

        errors = []
        for raw in emojis:
            parsed = self.parse_emoji(raw)
            try:
                await target_message.add_reaction(parsed)
            except discord.Forbidden:
                errors.append(f"{raw} (forbidden)")
            except discord.HTTPException as e:
                errors.append(f"{raw} (HTTP error: {e})")
            except Exception as e:
                errors.append(f"{raw} ({type(e).__name__})")

        if errors:
            await ctx.send(f"⚠️ Some reactions failed: {', '.join(errors)}")
        else:
            await ctx.send(
                f"✅ Added reactions {', '.join(emojis)} to [this message]({target_message.jump_url}) in {target_channel.mention}!"
            )

    @commands.command(
        name="unreact",
        help=("Remove one or more emoji reactions from a message.\n"
              "Usage: i!unreact message_id 😀 🎉 👍 <:custom:123> <a:anim:456>"))
    async def unreact(self,
                      ctx: commands.Context,
                      message_id: int = None,
                      *emojis):
        if message_id is None or not emojis:
            await ctx.send("❌ Usage:\n`i!unreact message_id 😀 🎉 👍`")
            return

        target_message, target_channel = await self._find_message(
            ctx, message_id)
        if not target_message or not target_channel:
            await ctx.send(
                "❌ Message not found. Ensure the message ID is valid and accessible."
            )
            return

        bot_member = self._bot_member_for_channel(target_channel)
        perms = target_channel.permissions_for(bot_member or ctx.me)

        removed = []
        not_found = []
        forbidden = []

        for raw in emojis:
            parsed = self.parse_emoji(raw)

            # Find if reaction exists on the message (compare string forms)
            found_reaction = None
            for r in target_message.reactions:
                if str(r.emoji) == str(parsed):
                    found_reaction = r
                    break

            if not found_reaction:
                not_found.append(raw)
                continue

            try:
                if perms.manage_messages:
                    await target_message.clear_reaction(parsed)
                else:
                    if bot_member is not None:
                        await target_message.remove_reaction(
                            parsed, bot_member)
                    else:
                        await target_message.clear_reaction(parsed)
                removed.append(raw)
            except discord.Forbidden:
                forbidden.append(raw)
            except discord.HTTPException as e:
                not_found.append(f"{raw} (HTTP error: {e})")
            except Exception as e:
                not_found.append(f"{raw} ({type(e).__name__})")

        parts = []
        if removed:
            parts.append(f"✅ Removed reactions: {', '.join(removed)}")
        if forbidden:
            parts.append(
                f"❌ Forbidden: {', '.join(forbidden)} (I lack permission to remove these.)"
            )
        if not_found:
            parts.append(
                f"⚠️ Reactions not found or failed: {', '.join(not_found)}")

        await ctx.send("\n".join(parts) if parts else
                       "⚠️ No matching reactions found to remove.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Reacts(bot))
