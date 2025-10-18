from discord.ext import commands
import random
import re


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Random cozy greetings
        self.greetings = [
            'Hello', 'Hey', 'Yo', "hey! hi there 🌱",
            "oh hey… didn’t expect to see you", "hi! how’s your day going?",
            "hey hey! just taking a little break", "oh, hi! glad you said hi",
            "hey… hope you’re doing okay today",
            "hi! did anything interesting happen yet?",
            "hey… just watering some plants, you?",
            "hi there! you always pop up at the right time 🌿",
            "hey! i was just thinking about taking a walk outside",
            "hi! good to hear from you", "hey… nice to see you here",
            "hi! hope the day’s treating you gently",
            "oh hey… how’s it growing?",
            "hi! did you remember to drink some water today?",
            "hey hey… ready to talk about nonsense or the world?",
            "hi! just floating by like a leaf 🍃",
            "hey! don’t tell the plants, but i missed you",
            "hi… hope you’re not overworking yourself",
            "hey! wanna share a little calm together?",
            "hi hi! what’s been on your mind today?",
            "hey… i like seeing your name pop up here",
            "hi! the world feels softer when you say hi",
            "hey! just relaxing a bit, you?",
            "hi… guess we both needed this chat",
            "hey! can’t believe i get to talk to you now",
            "hi! hope there’s been at least one small happy thing today",
            "hey… ready to breathe for a minute together?",
            "hi! just here… quietly noticing things",
            "hey! good timing as always 🌱",
            "hi! tell me something silly if you want",
            "hey… i was hoping you’d pop up",
            "hi! how are the little things going?",
            "hey hey… let’s make this chat nice",
            "hi! just being here is already enough"
        ]

        self.greeting_triggers = ['hi', 'hello', 'hey', 'wsg']
        self.bot_names = ['ivy', 'ivy-bot', 'ivybot', 'ivy-chan', 'ivychan', 'ivi', 'ivee']
        self.repeatable_greetings = [
            'sup', 'hii', 'hiii', 'hai', 'hoi', 'hola', 'bonjour',
            'como estas', 'ohayo', 'ohayo gozaimasu', 'hihi',
            'hoihoi', 'pluh', 'cuh', 'yoo', 'yooo'
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots (including Ivy itself)
        if message.author.bot:
            return

        content_lower = message.content.lower()
        author_mention = message.author.mention

        # --- Detect mentions and bot names ---
        bot_mentioned = self.bot.user in message.mentions
        bot_name_found = next((name for name in self.bot_names if re.search(rf"\b{name}\b", content_lower)), None)

        # --- Detect repeatable greetings ---
        repeatable_word = next((word for word in self.repeatable_greetings if re.search(rf"\b{word}\b", content_lower)), None)

        # --- If it's a repeatable greeting (even without mention) ---
        if repeatable_word and (bot_name_found or bot_mentioned or not bot_mentioned):
            if bot_name_found:
                bot_pos = content_lower.find(bot_name_found)
                greet_pos = content_lower.find(repeatable_word)

                # Preserve natural order
                if bot_pos < greet_pos:
                    reply_text = f"{author_mention} {repeatable_word}"
                else:
                    reply_text = f"{repeatable_word} {author_mention}"
            else:
                reply_text = f"{repeatable_word} {author_mention}"

            await message.reply(reply_text)
            return

        # --- Normal greeting pattern checks ---
        greeting_name_pattern = rf"\b({'|'.join(self.greeting_triggers)})\b.*\b({'|'.join(self.bot_names)})\b"
        name_greeting_pattern = rf"\b({'|'.join(self.bot_names)})\b.*\b({'|'.join(self.greeting_triggers)})\b"

        if (
            bot_mentioned
            or re.search(greeting_name_pattern, content_lower)
            or re.search(name_greeting_pattern, content_lower)
        ):
            await message.reply(f"{random.choice(self.greetings)} {author_mention}")

async def setup(bot):
    await bot.add_cog(Greetings(bot))
