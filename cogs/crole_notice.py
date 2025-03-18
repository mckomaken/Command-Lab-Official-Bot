import discord
from discord.ext import commands
from config.config import config


class Cmdbotlevel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return
        kake = message.guild.get_role(config.roles.kakedasi)
        syo = message.guild.get_role(config.roles.syokyuu)
        tyuu = message.guild.get_role(config.roles.tyuukyuu)
        zyou = message.guild.get_role(config.roles.zyoukyuu)
        if (kake and syo and tyuu and zyou) not in message.author.roles:
            await message.reply(f"<@{config.roles.kakedasi}>/<@{config.roles.kakedasi}>/<@{config.roles.kakedasi}>/<@{config.roles.kakedasi}>のうちのどれかがついていません\n<#{config.role_set_ch}>でロールを付けてきてください", silent=True, delete_after=15)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cmdbotlevel(bot))
