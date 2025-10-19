from discord.ext import commands
import discord


class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="react")
    async def react(self, ctx, channel: discord.TextChannel, message_id: int,
                    emoji: str):
        """
        Reacts to a message with a given emoji.
        Usage: i!react #channel message_id 😀
        """
        try:
            # Fetch the message
            message = await channel.fetch_message(message_id)

            # Add the emoji reaction
            await message.add_reaction(emoji)

            await ctx.send(
                f"✅ Added {emoji} reaction to the message in {channel.mention}!"
            )
        except discord.NotFound:
            await ctx.send("❌ Message not found.")
        except discord.Forbidden:
            await ctx.send("❌ I don’t have permission to add reactions.")
        except discord.HTTPException as e:
            await ctx.send(f"⚠️ Failed to add reaction: {e}")


# Setup function
async def setup(bot):
    await bot.add_cog(React(bot))
