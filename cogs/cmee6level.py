from datetime import datetime, timedelta

import discord
from discord.ext import commands

from config.config import config
from database import User, session


class CMee6level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.content.startswith("mee6level"):
            if message.channel.id == config.channels.level_data:  # 非公開mee6-level通知チャンネル
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

                mee6_channel = await self.bot.fetch_channel(config.channels.levelup)  # レベルアップ通知チャンネル
                levelupnoticeoff = message.guild.get_role(config.roles.levelupnoticeoff)
                lvupuser = await message.guild.fetch_member(userid)
                icon = "<:mee6_icon:1394152910182678610>"

                if level == 1 and levelupnoticeoff not in lvupuser.roles:
                    await mee6_channel.send(f"{text}{icon} /xp reached <@{userid}> mee6-level {level}\n-# メンション通知がうるさいと感じたら<#892255648295841842>で`MEE6レベル無効化`ロールを付けてね")
                    return

                userdisp = f"`{username}`" if levelupnoticeoff in lvupuser.roles else f"<@{userid}>"
                await mee6_channel.send(f"{text}{icon} /xp reached {userdisp} mee6-level {level}")
                userdb = session.query(User).filter_by(userid=userid).first()
                userdb.mee6level = level
                session.commit()

        elif message.content.startswith("mcmdlevel"):
            if message.channel.id == config.channels.level_data:  # 非公開mee6-level通知チャンネル
                userid = int(message.content.split(",")[1])  # userid表示
                username = str(message.content.split(",")[2])  # user名表示
                level = int(message.content.split(",")[3])  # レベル
                mcmd_5lv = message.guild.get_role(config.roles.mcmd_5lv)
                mcmd_15lv = message.guild.get_role(config.roles.mcmd_15lv)
                mcmd_30lv = message.guild.get_role(config.roles.mcmd_30lv)
                mcmd_300lv = message.guild.get_role(config.roles.mcmd_300lv)
                mcmd_600lv = message.guild.get_role(config.roles.mcmd_600lv)
                mcmd_1000lv = message.guild.get_role(config.roles.mcmd_1000lv)
                server_booster = message.guild.get_role(config.roles.serverbooster)
                lvupuser = await message.guild.fetch_member(userid)
                icon = "<:com2_i:834433852474392576>"

                if level >= 1000 and mcmd_1000lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_1000lv)
                    role_notice = "`コマ研警昇格候補者`ロール"
                elif level >= 600 and mcmd_600lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_600lv)
                    role_notice = "`メッセージピン止め権限`ロール"
                elif level >= 300 and mcmd_300lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_300lv)
                    role_notice = "`ロール色設定権限`ロール"
                elif level >= 30 and mcmd_30lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_30lv)
                    role_notice = "`宣伝権`ロール"
                elif level >= 15 and mcmd_15lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_15lv)
                    role_notice = "`サウンドボード使用権`ロール"
                elif level >= 5 and mcmd_5lv not in lvupuser.roles:
                    await lvupuser.add_roles(mcmd_5lv)
                    role_notice = "`Nitro特典使用権`ロール"
                elif server_booster in lvupuser.roles and (mcmd_5lv not in lvupuser.roles or mcmd_15lv not in lvupuser.roles):
                    await lvupuser.add_roles(mcmd_5lv)
                    await lvupuser.add_roles(mcmd_15lv)
                    role_notice = "`Nitro特典使用権`・`サウンドボード使用権`ロール(Server_Booster早期付与特典)"
                else:
                    role_notice = ""


                if userid == config.users.syunngiku:
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

                mee6_channel = await self.bot.fetch_channel(config.channels.levelup)  # 新たに作るmee6通知チャンネル
                levelupnoticeoff = message.guild.get_role(config.roles.levelupnoticeoff)
                userdisp = f"`{username}`" if levelupnoticeoff in lvupuser.roles else f"<@{userid}>"
                if role_notice != "":
                    await mee6_channel.send(f"{text}{icon} /xp reached {userdisp} mcmd-level {level}\n-# 新たに{role_notice}が付与されました!")
                else:
                    await mee6_channel.send(f"{text}{icon} /xp reached {userdisp} mcmd-level {level}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CMee6level(bot))
