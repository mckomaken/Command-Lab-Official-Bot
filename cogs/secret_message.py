from cryptography.fernet import Fernet
from discord import Message
from discord.ext import commands

from config.config import config


class CSecretMessage(commands.Cog):
    decrypted: dict[str, str]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        key = config.secret_message.key
        fernet = Fernet(key)
        fernet.encrypt("").hex()
        for k, v in config.secret_message.message.items():
            key = fernet.decrypt(k)
            value = fernet.decrypt(v)

            self.decrypted[key] = value

    @commands.Cog.listener
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        for k, v in self.decrypted.items():
            if message.clean_content == k:
                await message.reply(content=v)


async def setup(bot: commands.Bot):
    await bot.add_cog(CSecretMessage(bot))
