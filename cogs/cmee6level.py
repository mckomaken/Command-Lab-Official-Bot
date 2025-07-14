from discord.ext import commands
import discord
from config.config import config
from datetime import datetime, timedelta
from database import User, session


class CMee6level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.content.startswith("mee6level"):
            if message.channel.id in [config.mee6.botch]:  # 非公開mee6-level通知チャンネル
                userid = int(message.content.split(",")[1])  # userid表示
                username = str(message.content.split(",")[2])  # user名表示
                level = int(message.content.split(",")[3])  # レベル

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
                senndennkenn = message.guild.get_role(config.mee6.senndennkenn)
                hanabira = message.guild.get_role(config.mee6.hanabira)
                lvupuser = await message.guild.fetch_member(userid)
                jointime = int(datetime.now().timestamp() - lvupuser.joined_at.timestamp())
                admin_channel = await self.bot.fetch_channel(config.cmdbot_log)
                jointime1day = lvupuser.joined_at + timedelta(days=1)
                icon = "<:mee6_icon:1394152910182678610>"

                if level == 1 and levelupnoticeoff not in lvupuser.roles:
                    await mee6_channel.send(f"{text}{icon} /xp reached <@{userid}> mee6-level {level}\n-# メンション通知がうるさいと感じたら<#892255648295841842>で`MEE6レベル無効化`ロールを付けてね")
                    return
                elif level >= 5:
                    if senndennkenn not in lvupuser.roles and hanabira not in lvupuser.roles:
                        if jointime >= 86400:
                            await lvupuser.add_roles(senndennkenn)
                        else:
                            await admin_channel.send(f"<@{userid}>：宣伝権(仮)ロールを{jointime1day}に付与してください")

                userdisp = f"`{username}`" if levelupnoticeoff in lvupuser.roles else f"<@{userid}>"
                await mee6_channel.send(f"{text}{icon} /xp reached {userdisp} mee6-level {level}")
                userdb = session.query(User).filter_by(userid=userid).first()
                userdb.mee6level = level
                session.commit()

        elif message.content.startswith("mcmdlevel"):
            if message.channel.id in [config.mee6.botch]:  # 非公開mee6-level通知チャンネル
                userid = int(message.content.split(",")[1])  # userid表示
                username = str(message.content.split(",")[2])  # user名表示
                level = int(message.content.split(",")[3])  # レベル
                mcmdlv_5 = message.guild.get_role(config.mee6.mcmdlv_5)
                lvupuser = await message.guild.fetch_member(userid)
                icon = "<:com2_i:834433852474392576>"

                if level >= 5:
                    if mcmdlv_5 not in lvupuser.roles:
                        await lvupuser.add_roles(mcmdlv_5)

                if userid == config.syunngikuid:
                    return
                elif level <= 0:
                    return
                elif (level % 500 == 0):
                    text = "# "
                elif (level % 100 == 0):
                    text = "## "
                elif (level % 50 == 0):
                    text = "### "
                elif (level % 10 == 0):
                    text = ""
                else:
                    return

                mee6_channel = await self.bot.fetch_channel(config.mee6.levelup)  # 新たに作るmee6通知チャンネル
                levelupnoticeoff = message.guild.get_role(config.mee6.levelupnoticeoff)
                userdisp = f"`{username}`" if levelupnoticeoff in lvupuser.roles else f"<@{userid}>"
                await mee6_channel.send(f"{text}{icon} /xp reached {userdisp} mcmd-level {level}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CMee6level(bot))
