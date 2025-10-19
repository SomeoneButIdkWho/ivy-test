from discord.ext import commands
import discord


class Reply(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help=
        "Reply to a specific message by its ID. Usage:\n i!reply message_id your reply\nOR\n i!reply #channel message_id your reply"
    )
    async def reply(self,
                    ctx,
                    message_id: int = None,
                    *,
                    reply_text: str = None):
        if message_id is None or reply_text is None:
            await ctx.send(
                "❌ Usage:\n`i!reply message_id your reply`\nor\n`i!reply #channel message_id your reply`"
            )
            return

        target_message = None
        target_channel = None
        # Try to get the channel from context (if command invoked in a text channel)
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
            await ctx.send(
                "❌ Message not found. Ensure the message ID is valid and accessible."
            )
            return

        # Check bot permissions
        if not target_channel.permissions_for(ctx.me).send_messages:
            await ctx.send(
                "❌ I do not have permission to send messages in the channel containing that message."
            )
            return

        try:
            await target_message.reply(reply_text)
            await ctx.send(f"✅ Replied in {target_channel.mention}")
        except discord.Forbidden:
            await ctx.send(
                "❌ I do not have permission to reply to that message.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to send reply: {e}")


async def setup(bot):
    await bot.add_cog(Reply(bot))
