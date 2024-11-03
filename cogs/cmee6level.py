from discord.ext import commands
import discord
from config.config import config


class CMee6level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if "mee6level" in message.content:
            if message.channel.id in [config.mee6.botch]:  # 非公開mee6-level通知チャンネル
                userid = message.content.split(",")[1]  # userid表示
                username = message.content.split(",")[2]  # user名表示
                level = message.content.split(",")[3]  # レベル
                if (level % 50 == 0):
                    text = "# "
                elif (level % 10 == 0):
                    text = "## "
                elif (level % 5 == 0):
                    text = "### "
                else:
                    text = ""
                mee6_channel = await self.bot.fetch_channel(config.mee6.levelup)  # 新たに作るmee6通知チャンネル
                if message.author.roles in [config.mee6.levelupnoticeoff]:  # mee6levelup無効化ロールを持っているかどうか
                    await mee6_channel.send(f"{text}/xp reached {username} level {level}")
                else:
                    await mee6_channel.send(f"{text}/xp reached <@{userid}> level {level}")
                    

async def setup(bot: commands.Bot):
    await bot.add_cog(CMee6level(bot))
