from discord.ext import commands
import discord
import re
import asyncio

MAX_PURGE = 500  # max messages per purge
CONFIRM_THRESHOLD = 50  # messages above this trigger confirmation

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirm_action(self, ctx, count: int):
        """Ask user for confirmation before purging large amounts."""
        msg = await ctx.send(f"⚠️ You are about to delete {count} messages. Confirm? ✅ / ❌")

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            if str(reaction.emoji) == "✅":
                return True
            else:
                await ctx.send("❌ Purge cancelled.", delete_after=5)
                return False
        except asyncio.TimeoutError:
            await ctx.send("⌛ Confirmation timed out. Purge cancelled.", delete_after=5)
            return False

    async def safe_purge(self, ctx, amount: int, check=None):
        """Handle max limit, confirmation, and purge execution."""
        amount = min(amount, MAX_PURGE)

        if amount > CONFIRM_THRESHOLD:
            confirmed = await self.confirm_action(ctx, amount)
            if not confirmed:
                return 0

        deleted = await ctx.channel.purge(limit=amount, check=check)
        return len(deleted)

    # 🧹 Base purge
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        deleted_count = await self.safe_purge(ctx, amount + 1)
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count-1} messages.", delete_after=5)

    # 👤 Purge by user
    @purge.command(name="user")
    @commands.has_permissions(manage_messages=True)
    async def purge_user(self, ctx, member: discord.Member, amount: int = 100):
        deleted_count = await self.safe_purge(ctx, amount, check=lambda m: m.author == member)
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} messages from {member.display_name}.", delete_after=5)

    # 🧾 Purge by keyword
    @purge.command(name="contains")
    @commands.has_permissions(manage_messages=True)
    async def purge_contains(self, ctx, *, keyword: str):
        deleted_count = await self.safe_purge(ctx, MAX_PURGE, check=lambda m: keyword.lower() in m.content.lower())
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} messages containing '{keyword}'.", delete_after=5)

    # 🤖 Purge bot messages
    @purge.command(name="bots")
    @commands.has_permissions(manage_messages=True)
    async def purge_bots(self, ctx, amount: int = 100):
        deleted_count = await self.safe_purge(ctx, amount, check=lambda m: m.author.bot)
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} bot messages.", delete_after=5)

    # 🧍 Purge human messages
    @purge.command(name="humans")
    @commands.has_permissions(manage_messages=True)
    async def purge_humans(self, ctx, amount: int = 100):
        deleted_count = await self.safe_purge(ctx, amount, check=lambda m: not m.author.bot)
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} human messages.", delete_after=5)

    # 📎 Purge messages with attachments
    @purge.command(name="attachments")
    @commands.has_permissions(manage_messages=True)
    async def purge_attachments(self, ctx, amount: int = 100):
        deleted_count = await self.safe_purge(ctx, amount, check=lambda m: len(m.attachments) > 0)
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} messages with attachments.", delete_after=5)

    # 🔗 Purge messages with links
    @purge.command(name="links")
    @commands.has_permissions(manage_messages=True)
    async def purge_links(self, ctx, amount: int = 100):
        url_pattern = re.compile(r'https?://')
        deleted_count = await self.safe_purge(ctx, amount, check=lambda m: bool(url_pattern.search(m.content)))
        if deleted_count:
            await ctx.send(f"✅ Deleted {deleted_count} messages containing links.", delete_after=5)

    # ❌ Handle missing permissions
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You don’t have permission to manage messages.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Usage: `i!purge <amount>` or `i!purge <subcommand>`", delete_after=5)
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Purge(bot))
