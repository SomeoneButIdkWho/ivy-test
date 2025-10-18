from discord.ext import commands
import random
import re


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.greetings = [
            'Hello', 'Hey', 'Yo', "hey! hi there 🌱",
            "oh hey… didn't expect to see you", "hi! how's your day going?",
            "hey hey! just taking a little break", "oh, hi! glad you said hi",
            "hey… hope you're doing okay today",
            "hi! did anything interesting happen yet?",
            "hey… just watering some plants, you?",
            "hi there! you always pop up at the right time 🌿",
            "hey! i was just thinking about taking a walk outside",
            "hi! good to hear from you", "hey… nice to see you here",
            "hi! hope the day's treating you gently",
            "oh hey… how's it growing?",
            "hi! did you remember to drink some water today?",
            "hey hey… ready to talk about nonsense or the world?",
            "hi! just floating by like a leaf 🍃",
            "hey! don't tell the plants, but i missed you",
            "hi… hope you're not overworking yourself",
            "hey! wanna share a little calm together?",
            "hi hi! what's been on your mind today?",
            "hey… i like seeing your name pop up here",
            "hi! the world feels softer when you say hi",
            "hey! just relaxing a bit, you?",
            "hi… guess we both needed this chat",
            "hey! can't believe i get to talk to you now",
            "hi! hope there's been at least one small happy thing today",
            "hey… ready to breathe for a minute together?",
            "hi! just here… quietly noticing things",
            "hey! good timing as always 🌱",
            "hi! tell me something silly if you want",
            "hey… i was hoping you'd pop up",
            "hi! how are the little things going?",
            "hey hey… let's make this chat nice",
            "hi! just being here is already enough"
        ]

        self.greeting_triggers = ['hi', 'hello', 'hey', 'wsg']
        self.bot_names = [
            'ivy', 'ivy-bot', 'ivybot', 'ivy-chan', 'ivychan', 'ivi', 'ivee'
        ]
        self.repeatable_greetings = [
            'sup', 'hii', 'hiii', 'hai', 'hoi', 'hola', 'bonjour',
            'como estas', 'ohayo', 'ohayo gozaimasu', 'hihi', 'hoihoi', 'pluh',
            'cuh', 'yoo', 'yooo'
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

        repeatable_word = next((word for word in self.repeatable_greetings
                                if re.search(rf"\b{word}\b", content_lower)),
                               None)
        if repeatable_word and (bot_mentioned or bot_name_found):
            await message.reply(f"{repeatable_word} {author_mention}")
            return

        greeting_name_pattern = rf"\b({'|'.join(self.greeting_triggers)})\b.*\b({'|'.join(self.bot_names)})\b"
        name_greeting_pattern = rf"\b({'|'.join(self.bot_names)})\b.*\b({'|'.join(self.greeting_triggers)})\b"

        if ((re.search(greeting_name_pattern, content_lower) or re.search(
                name_greeting_pattern, content_lower) or bot_mentioned)
                and content_lower.strip() not in self.bot_names):
            await message.reply(
                f"{random.choice(self.greetings)} {author_mention}")


async def setup(bot):
    await bot.add_cog(Greetings(bot))
