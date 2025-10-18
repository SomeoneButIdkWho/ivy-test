from discord.ext import commands
import discord


class Reply(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx, channel: discord.TextChannel, message_id: int,
                    *, reply_text):
        try:
            target_message = await channel.fetch_message(message_id)
            await target_message.reply(reply_text)
            await ctx.send(f"✅ Replied in {channel.mention}")
        except discord.NotFound:
            await ctx.send("❌ Message not found. Make sure the ID is correct.")
        except discord.Forbidden:
            await ctx.send(
                "❌ I do not have permission to access that channel or reply.")
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to send reply: {e}")


async def setup(bot):
    await bot.add_cog(Reply(bot))
