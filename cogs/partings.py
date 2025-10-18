from discord.ext import commands
import random
import re


class Farewell(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.farewells = [
            "Bye bye! 🌿", "See you later!", "Take care!",
            "Goodbye… come back soon!", "Catch you later!", "Bye! 👋",
            "See ya! 🌱", "Farewell… until next time", "Stay well!"
        ]

        self.farewell_triggers = [
            'bye', 'goodbye', 'cya', 'see ya', 'farewell'
        ]
        self.bot_names = [
            'ivy', 'ivy-bot', 'ivybot', 'ivy-chan', 'ivychan', 'ivi', 'ivee'
        ]
        self.repeatable_farewells = [
            'bye', 'byee', 'byeee', 'cya', 'see ya', 'see yaa'
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content_lower = message.content.lower()
        author_mention = message.author.mention
        bot_mentioned = self.bot.user in message.mentions
        bot_name_found = any(
            re.search(rf"\b{name}\b", content_lower)
            for name in self.bot_names)

        repeatable_word = next((word for word in self.repeatable_farewells
                                if re.search(rf"\b{word}\b", content_lower)),
                               None)
        if repeatable_word and (bot_mentioned or bot_name_found):
            await message.reply(f"{repeatable_word} {author_mention}")
            return

        # Only reply if a trigger word AND the bot name are present
        farewell_name_pattern = rf"\b({'|'.join(self.farewell_triggers)})\b.*\b({'|'.join(self.bot_names)})\b"
        name_farewell_pattern = rf"\b({'|'.join(self.bot_names)})\b.*\b({'|'.join(self.farewell_triggers)})\b"

        if (re.search(farewell_name_pattern, content_lower)
                or re.search(name_farewell_pattern, content_lower)
            ) and content_lower.strip() not in self.bot_names:
            await message.reply(
                f"{random.choice(self.farewells)} {author_mention}")

        if bot_mentioned or bot_name_found or re.search(
                farewell_name_pattern, content_lower) or re.search(
                    name_farewell_pattern, content_lower):
            await message.reply(
                f"{random.choice(self.farewells)} {author_mention}")


async def setup(bot):
    await bot.add_cog(Farewell(bot))
