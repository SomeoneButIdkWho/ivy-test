from discord.ext import commands
import random
import re


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.greetings = ['Hello', 'Hey', 'Yo']
        self.greeting_triggers = [
            'hi',
            'hello',
            'hey',
            'wsg',
        ]
        self.bot_names = [
            'ivy', 'ivy-bot', 'ivybot', 'ivy-chan', 'ivychan', 'ivi', 'ivee'
        ]
        self.repeatable_greetings = [
            'sup', 'yo', 'hii', 'hiii', 'hai', 'hoi', 'hola', 'bonjour',
            'como estas', 'ohayo', 'ohayo gozaimasu', 'hihi', 'hoihoi', 'pluh',
            'cuh', 'yoo', 'yooo'
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content_lower = message.content.lower()
        author_mention = message.author.mention

        bot_mentioned = self.bot.user in message.mentions

        greeting_name_pattern = rf"\b({'|'.join(self.greeting_triggers + self.repeatable_greetings)})\b.*\b({'|'.join(self.bot_names)})\b"
        name_greeting_pattern = rf"\b({'|'.join(self.bot_names)})\b.*\b({'|'.join(self.greeting_triggers + self.repeatable_greetings)})\b"
        greeting_with_name = re.search(greeting_name_pattern, content_lower)
        name_with_greeting = re.search(name_greeting_pattern, content_lower)

        repeatable_word = None
        for word in self.repeatable_greetings:
            if re.search(rf"\b{word}\b", content_lower):
                repeatable_word = word
                break

        should_respond = bot_mentioned or greeting_with_name or name_with_greeting or repeatable_word

        if should_respond:
            if repeatable_word:
                if any(bot_name in content_lower
                       for bot_name in self.bot_names):
                    if any(
                            content_lower.startswith(bot_name)
                            for bot_name in self.bot_names):
                        reply = f"{author_mention} {repeatable_word}"
                    else:
                        reply = f"{repeatable_word} {author_mention}"
                else:
                    reply = f"{repeatable_word} {author_mention}"
                await message.channel.send(reply)
                return
            await message.channel.send(
                f"{random.choice(self.greetings)} {author_mention}")


async def setup(bot):
    await bot.add_cog(Greetings(bot))
