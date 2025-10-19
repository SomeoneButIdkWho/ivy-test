import asyncio
from discord.ext import commands


class Spam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.DEFAULT_DELAY = 0.5
        self.MAX_MESSAGES = 100
        self.active_spams = {}  # track active spam tasks per channel

    @commands.group(
        name="spam",
        invoke_without_command=True,
        help=
        "Send a burst of messages. Usage: `!spam <count> [delay] [#channel] <message>`"
    )
    async def spam(self, ctx, count: int = None, *args):
        if count is None:
            await ctx.send(
                "You must provide a count. Usage: `!spam <count> [delay] [#channel] <message>`"
            )
            return
        await self._spam_messages(ctx, count, args, count_mode=False)

    @spam.command(name="count",
                  help="Spam messages with a count prefix (1:, 2:, …)")
    async def spam_count(self, ctx, count: int = None, *args):
        if count is None:
            await ctx.send(
                "You must provide a count. Usage: `!spam count <count> [delay] [#channel] <message>`"
            )
            return
        await self._spam_messages(ctx, count, args, count_mode=True)

    async def _spam_messages(self, ctx, count, args, count_mode=False):
        delay = self.DEFAULT_DELAY
        channel = ctx.channel
        message_content = None

        if not args:
            await ctx.send("You must provide a message to spam.")
            return

        # Check if first arg is a float (delay)
        try:
            potential_delay = float(args[0])
            delay = potential_delay
            args = args[1:]
        except (ValueError, TypeError):
            pass

        # Check if first arg is a channel mention
        if args and args[0].startswith("<#") and args[0].endswith(">"):
            try:
                channel_id = int(args[0][2:-1])
                new_channel = ctx.guild.get_channel(channel_id)
                if new_channel is None:
                    await ctx.send("Invalid channel specified.")
                    return
                channel = new_channel
                args = args[1:]
            except Exception:
                await ctx.send("Could not parse channel mention.")
                return

        # Remaining args are the message
        if args:
            message_content = " ".join(args).strip()
        else:
            await ctx.send("You must provide a message to spam.")
            return

        # Validate limits
        if count <= 0:
            await ctx.send("`count` must be positive.")
            return
        if count > self.MAX_MESSAGES:
            await ctx.send(
                f"`count` capped to {self.MAX_MESSAGES} to avoid abuse.")
            count = self.MAX_MESSAGES
        if delay < 0.05:
            await ctx.send("Delay too small, using minimum delay 0.05s.")
            delay = 0.05

        if message_content == "":
            await ctx.send("You must provide a message to spam.")
            return

        if channel.id in self.active_spams:
            await ctx.send(
                f"Spam already running in {channel.mention}! Cancel it first with `!spam cancel`."
            )
            return

        status = await ctx.send(
            f"Spamming **{count}** messages in {channel.mention} with {delay}s delay..."
        )

        task = asyncio.create_task(
            self._send_spam(channel, message_content, count, delay, status,
                            count_mode))
        self.active_spams[channel.id] = task

    async def _send_spam(self, channel, message_content, count, delay,
                         status_message, count_mode):
        sent = 0
        try:
            for i in range(1, count + 1):
                content = f"{i}: {message_content}" if count_mode else message_content
                await channel.send(content)
                sent += 1
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            await status_message.edit(
                content=
                f"Spam cancelled after sending {sent} messages in {channel.mention}."
            )
            self.active_spams.pop(channel.id, None)
            return
        except Exception as e:
            await status_message.edit(
                content=f"Stopped after sending {sent} messages. Error: {e}")
            self.active_spams.pop(channel.id, None)
            return

        await status_message.edit(
            content=
            f"Done — sent {sent} messages in {channel.mention} (delay {delay}s)."
        )
        self.active_spams.pop(channel.id, None)

    @spam.command(name="cancel", help="Cancel an active spam in this channel")
    async def spam_cancel(self, ctx):
        task = self.active_spams.get(ctx.channel.id)
        if task:
            task.cancel()
            await ctx.send("Spam cancelled.")
        else:
            await ctx.send("No active spam in this channel.")


def setup(bot):
    bot.add_cog(Spam(bot))
