from discord.ext import commands
import discord
import re


class Reply(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx, channel: discord.TextChannel, message_id: int,
                    *, reply_text):
        """
        Reply to a specific message in a channel.
        Usage: i!reply #channel message_id Your reply here
        """
        try:
            # Fetch the message by ID
            target_message = await channel.fetch_message(message_id)
            await target_message.reply(reply_text)
            await ctx.send(f"✅ Replied to message in {channel.mention}")
        except discord.NotFound:
            await ctx.send("❌ Could not find the message with that ID.")
        except discord.Forbidden:
            await ctx.send(
                "❌ I do not have permission to read or send messages in that channel."
            )
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to send reply: {e}")


async def setup(bot):
    await bot.add_cog(Reply(bot))
