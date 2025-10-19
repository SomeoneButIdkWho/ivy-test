from discord.ext import commands
import discord


class Unreact(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help=
        "Remove one or more emoji reactions from a message.\nUsage: i!unreact message_id 😀 🎉 👍"
    )
    async def unreact(self, ctx, message_id: int = None, *emojis):
        """
        Removes specific emoji reactions from a message.
        Usage: i!unreact message_id 😀 🎉 👍
        """
        if message_id is None or not emojis:
            await ctx.send("❌ Usage:\n`i!unreact message_id 😀 🎉 👍`")
            return

        target_message = None
        target_channel = None

        try:
            target_message = await ctx.channel.fetch_message(message_id)
            target_channel = ctx.channel
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        # Search across all text channels if not found
        if not target_message and ctx.guild:
            for channel in ctx.guild.text_channels:
                perms = channel.permissions_for(ctx.me)
                if not (perms.read_messages and perms.read_message_history):
                    continue
                try:
                    message = await channel.fetch_message(message_id)
                    target_message = message
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

        # Permission check
        if not target_channel.permissions_for(ctx.me).manage_messages:
            await ctx.send(
                "❌ I don’t have permission to remove reactions in that channel."
            )
            return

        removed = []
        not_found = []

        for emoji in emojis:
            # Accept both Unicode and custom emoji (string or Emoji object)
            reaction = discord.utils.get(target_message.reactions, emoji=emoji)
            if reaction:
                try:
                    await target_message.clear_reaction(emoji)
                    removed.append(emoji)
                except discord.Forbidden:
                    not_found.append(f"{emoji} (forbidden)")
                except discord.HTTPException:
                    not_found.append(f"{emoji} (HTTP error)")
            else:
                not_found.append(emoji)

        result_msg = []
        if removed:
            result_msg.append(
                f"✅ Removed reactions: {', '.join(removed)} from [this message]({target_message.jump_url})"
            )
        if not_found:
            result_msg.append(
                f"⚠️ Reactions not found or not removable: {', '.join(not_found)}"
            )

        await ctx.send("\n".join(result_msg))


# Setup function
async def setup(bot):
    await bot.add_cog(Unreact(bot))
