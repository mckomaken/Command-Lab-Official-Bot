import discord
from discord.ext import commands

from config.config import config


class Rolenotice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return
        if message.channel.id == config.channels.authentication:
            return
        kake = message.guild.get_role(config.roles.newbie)
        syo = message.guild.get_role(config.roles.beginner)
        tyuu = message.guild.get_role(config.roles.intermediate)
        zyou = message.guild.get_role(config.roles.advanced)
        je = message.guild.get_role(config.roles.java_edition)
        be = message.guild.get_role(config.roles.bedrock_edition)
        pc = message.guild.get_role(config.roles.computer)
        sumaho = message.guild.get_role(config.roles.smartphone)
        gameki = message.guild.get_role(config.roles.console)
        role_ch = await self.bot.fetch_channel(config.channels.role_set)

        comlank = ""
        jebe = ""
        kisyu = ""
        send = False

        if kake not in message.author.roles and syo not in message.author.roles and tyuu not in message.author.roles and zyou not in message.author.roles:
            comlank = f"> {kake.mention}/{syo.mention}/{tyuu.mention}/{zyou.mention}のうち1つ\n"
            send = True
        if je not in message.author.roles and be not in message.author.roles:
            jebe = f"> {je.mention}/{be.mention}のうち1つ\n"
            send = True
        if pc not in message.author.roles and sumaho not in message.author.roles and gameki not in message.author.roles:
            kisyu = f"> {pc.mention}/{sumaho.mention}/{gameki.mention}のうち1つ\n"
            send = True
        if send is True:
            await message.reply(f"以下のロールが付いていません\n{comlank}{jebe}{kisyu}<#{config.channels.role_set}>でロールを付けてきてください\n-# なおこのメッセージは10秒後に消えます", silent=True, delete_after=10, allowed_mentions=discord.AllowedMentions(roles=False))
            await role_ch.send(f"{message.author.mention}\nこちらのチャンネルの上部で\n{comlank}{jebe}{kisyu}対応するボタンを押して、ロールを付けてきてください\n-# なおこのメッセージは20秒後に消えます", silent=True, delete_after=20, allowed_mentions=discord.AllowedMentions(roles=False))
        else:
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(Rolenotice(bot))
