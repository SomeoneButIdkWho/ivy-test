from discord.ext import commands
import discord
import re

MAX_PURGE = 250  # maximum messages to delete at once

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🧹 Base purge command group
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Delete a number of recent messages."""
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ Deleted {len(deleted)-1} messages.", delete_after=5)

    # 👤 Purge by user
    @purge.command(name="user")
    @commands.has_permissions(manage_messages=True)
    async def purge_user(self, ctx, member: discord.Member, amount: int = 100):
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        def check(msg):
            return msg.author == member
        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f"✅ Deleted {len(deleted)} messages from {member.display_name}.", delete_after=5)

    # 🧾 Purge by keyword
    @purge.command(name="contains")
    @commands.has_permissions(manage_messages=True)
    async def purge_contains(self, ctx, *, keyword: str):
        deleted = await ctx.channel.purge(limit=MAX_PURGE, check=lambda m: keyword.lower() in m.content.lower())
        await ctx.send(f"✅ Deleted {len(deleted)} messages containing '{keyword}'.", delete_after=5)

    # 🤖 Purge bot messages
    @purge.command(name="bots")
    @commands.has_permissions(manage_messages=True)
    async def purge_bots(self, ctx, amount: int = 100):
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author.bot)
        await ctx.send(f"✅ Deleted {len(deleted)} bot messages.", delete_after=5)

    # 🧍 Purge human messages
    @purge.command(name="humans")
    @commands.has_permissions(manage_messages=True)
    async def purge_humans(self, ctx, amount: int = 100):
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: not m.author.bot)
        await ctx.send(f"✅ Deleted {len(deleted)} human messages.", delete_after=5)

    # 📎 Purge messages with attachments
    @purge.command(name="attachments")
    @commands.has_permissions(manage_messages=True)
    async def purge_attachments(self, ctx, amount: int = 100):
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: len(m.attachments) > 0)
        await ctx.send(f"✅ Deleted {len(deleted)} messages with attachments.", delete_after=5)

    # 🔗 Purge messages with links
    @purge.command(name="links")
    @commands.has_permissions(manage_messages=True)
    async def purge_links(self, ctx, amount: int = 100):
        if amount > MAX_PURGE:
            await ctx.send(f"⚠️ You can only delete up to {MAX_PURGE} messages at a time.", delete_after=5)
            return
        url_pattern = re.compile(r'https?://')
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: bool(url_pattern.search(m.content)))
        await ctx.send(f"✅ Deleted {len(deleted)} messages containing links.", delete_after=5)

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
