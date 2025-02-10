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
                userid = int(message.content.split(",")[1])  # userid表示
                username = str(message.content.split(",")[2])  # user名表示
                level = int(message.content.split(",")[3])  # レベル
                print(f"id:{userid}, name:{username}, lv:{level}")
                if (level % 50 == 0):
                    text = "# "
                elif (level % 10 == 0):
                    text = "## "
                elif (level % 5 == 0):
                    text = "### "
                else:
                    text = ""
                mee6_channel = await self.bot.fetch_channel(config.mee6.levelup)  # 新たに作るmee6通知チャンネル
                levelupnoticeoff = message.guild.get_role(config.mee6.levelupnoticeoff)
                # senndennkenn = message.guild.get_role(config.mee6.senndennkenn)
                lvupuser = await message.guild.fetch_member(userid)
                if levelupnoticeoff not in lvupuser.roles:
                    if level == 1:
                        await mee6_channel.send(f"{text}/xp reached <@{userid}> level {level}\n-# メンション通知がうるさいと感じたら<#892255648295841842>で`MEE6レベル無効化`ロールを付けてね")
                    # elif level >= 5 and senndennkenn not in lvupuser.roles:
                    # await lvupuser.add_roles(senndennkenn)
                    # await mee6_channel.send(f"{text}/xp reached <@{userid}> level {level}")
                    else:
                        await mee6_channel.send(f"{text}/xp reached <@{userid}> level {level}")
                else:
                    # if level >= 5 and senndennkenn not in lvupuser.roles:
                    # await lvupuser.add_roles(senndennkenn)
                    # await mee6_channel.send(f"{text}/xp reached `{username}` level {level}")
                    # else:
                    # await mee6_channel.send(f"{text}/xp reached `{username}` level {level}")
                    await mee6_channel.send(f"{text}/xp reached `{username}` level {level}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CMee6level(bot))
