from discord.ext import commands
import discord


class Reply(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Reply to a message: i!reply #channel message_id reply text")
    async def reply(self,
                    ctx,
                    channel: discord.TextChannel = None,
                    message_id: int = None,
                    *,
                    reply_text: str = None):
        # Argument validation
        if channel is None or message_id is None or reply_text is None:
            await ctx.send(
                "❌ Usage: `i!reply #channel message_id reply text`\nExample: `i!reply #general 123456789012345678 Thanks!`"
            )
            return

        # Permission check
        if not channel.permissions_for(ctx.me).send_messages:
            await ctx.send(
                "❌ I do not have permission to send messages in that channel.")
            return

        try:
            target_message = await channel.fetch_message(message_id)
            await target_message.reply(reply_text)
            await ctx.send(f"✅ Replied in {channel.mention}")
        except discord.NotFound:
            await ctx.send(
                "❌ Message not found. Make sure the channel and message ID are correct."
            )
        except discord.Forbidden:
            await ctx.send(
                "❌ I do not have permission to access that channel or reply.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to send reply: {e}")


async def setup(bot):
    await bot.add_cog(Reply(bot))
