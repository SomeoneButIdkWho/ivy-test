from discord.ext import commands
import discord

class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="React to a message with one or more emojis. Usage:\n i!react message_id 😀 🎉 👍"
    )
    async def react(self, ctx, message_id: int = None, *emojis):
        """
        Reacts to a message with all given emojis.
        Usage: i!react message_id 😀 🎉 👍
        """
        if message_id is None or not emojis:
            await ctx.send(
                "❌ Usage:\n`i!react message_id 😀 🎉 👍`"
            )
            return

        target_message = None
        target_channel = None

        # Try to fetch in current channel first
        if isinstance(ctx.channel, discord.TextChannel):
            try:
                target_message = await ctx.channel.fetch_message(message_id)
                target_channel = ctx.channel
            except discord.NotFound:
                target_message = None

        # If not found in current channel, search all accessible text channels
        if not target_message:
            for channel in ctx.guild.text_channels:
                try:
                    message = await channel.fetch_message(message_id)
                    target_message = message
                    target_channel = channel
                    break
                except discord.NotFound:
                    continue
                except discord.Forbidden:
                    continue

        if not target_message or not target_channel:
            await ctx.send("❌ Message not found. Ensure the message ID is valid and accessible.")
            return

        # Permission check
        if not target_channel.permissions_for(ctx.me).add_reactions:
            await ctx.send("❌ I do not have permission to add reactions in that channel.")
            return

        errors = []
        for emoji in emojis:
            try:
                await target_message.add_reaction(emoji)
            except discord.HTTPException as e:
                errors.append(f"{emoji} ({e})")
            except discord.Forbidden:
                errors.append(f"{emoji} (forbidden)")
            except Exception as e:
                errors.append(f"{emoji} ({e})")

        if errors:
            await ctx.send(f"⚠️ Some reactions failed: {', '.join(errors)}")
        else:
            await ctx.send(
                f"✅ Added reactions {', '.join(emojis)} to [this message]({target_message.jump_url}) in {target_channel.mention}!"
            )

# Setup function
async def setup(bot):
    await bot.add_cog(React(bot))
