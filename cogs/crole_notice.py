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
        if message.channel.id == config.ninnsyouch:
            return
        kake = message.guild.get_role(config.roles.kakedasi)
        syo = message.guild.get_role(config.roles.syokyuu)
        tyuu = message.guild.get_role(config.roles.tyuukyuu)
        zyou = message.guild.get_role(config.roles.zyoukyuu)
        je = message.guild.get_role(config.roles.jezei)
        be = message.guild.get_role(config.roles.bezei)
        pc = message.guild.get_role(config.roles.personalcomputer)
        sumaho = message.guild.get_role(config.roles.smartphone)
        gameki = message.guild.get_role(config.roles.gamemachine)

        if kake not in message.author.roles and syo not in message.author.roles and tyuu not in message.author.roles and zyou not in message.author.roles:
            await message.reply(f"{kake.mention}/{syo.mention}/{tyuu.mention}/{zyou.mention}のうちのどれかがついていません\n<#{config.role_set_ch}>でロールを付けてきてください", silent=True, delete_after=10)
        if je not in message.author.roles and be not in message.author.roles:
            await message.reply(f"{je.mention}/{be.mention}のうちのどれかがついていません\n<#{config.role_set_ch}>でロールを付けてきてください", silent=True, delete_after=10)
        if pc not in message.author.roles and sumaho not in message.author.roles and gameki not in message.author.roles:
            await message.reply(f"{pc.mention}/{sumaho.mention}/{gameki.mention}のうちのどれかがついていません\n<#{config.role_set_ch}>でロールを付けてきてください", silent=True, delete_after=10)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cmdbotlevel(bot))
