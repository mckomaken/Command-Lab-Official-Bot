import discord
from discord import app_commands
from discord.ext import commands
from database import User, session
from config.config import config


class Cmdbotlevelcom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="clevel", description="コマ研レベルの表示")
    @app_commands.describe(target="ユーザー名")
    async def clevel(self, interaction: discord.Interaction, target: discord.Member = None):
        if target is None:
            userdb = session.query(User).filter_by(userid=interaction.user.id).first()
            if not userdb:
                await interaction.response.send_message("あなたはまだ経験値を獲得していません\n### 喋ろう!!!!!")
            else:
                level_embed = discord.Embed(
                    title=f"{interaction.user.display_name}のレベル",
                    description=f"```go\nレベル: {userdb.level} lv\n経験値: {userdb.exp} exp\n{userdb.level + 1}lvまであと {10000 - userdb.exp} exp\n```",
                    color=0x6fb7ff
                )
                level_embed.add_field(name="総獲得経験値量", value=f"```py\n{userdb.alladdexp} exp\n```", inline=True)
                level_embed.add_field(name="総損失経験値量", value=f"```py\n{userdb.allremoveexp} exp\n```", inline=True)
                level_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=level_embed)
                userdb.allexp = (userdb.level * 10000) + userdb.exp
                session.commit()
        else:
            targetdb = session.query(User).filter_by(userid=target.id).first()
            if not targetdb:
                await interaction.response.send_message(f"`{target.display_name}`はまだ経験値を獲得していません\n### 喋らせよう!!!!!(笑)")
            else:
                level_embed = discord.Embed(
                    title=f"{target.display_name}のレベル",
                    description=f"```go\nレベル: {targetdb.level} lv\n経験値: {targetdb.exp} exp\n{targetdb.level + 1}lvまであと {10000 - targetdb.exp} exp\n```",
                    color=0x6fb7ff
                )
                level_embed.add_field(name="総獲得経験値量", value=f"```py\n{targetdb.alladdexp} exp\n```", inline=True)
                level_embed.add_field(name="総損失経験値量", value=f"```py\n{targetdb.allremoveexp} exp\n```", inline=True)
                level_embed.set_author(name=target.display_name, icon_url=target.avatar.url)
                await interaction.response.send_message(embed=level_embed)
                targetdb.allexp = (targetdb.level * 10000) + targetdb.exp
                session.commit()

    @app_commands.command(name="cgivexp", description="他人に経験値付与")
    @app_commands.describe(target="ユーザー名", givexp="相手に与える経験値量")
    async def cgivexp(self, interaction: discord.Interaction, target: discord.Member, givexp: int):
        givedb = session.query(User).filter_by(userid=interaction.user.id).first()
        targetdb = session.query(User).filter_by(userid=target.id).first()
        if givedb.dailygivexp is True:
            await interaction.response.send_message("今日はもうあげられないよ", ephemeral=True)
            return
        if 0 >= givexp or givexp >= 5000:
            await interaction.response.send_message("引数:givexpは1以上4999以下を指定してください", ephemeral=True)
            return
        if not givedb:
            await interaction.response.send_message(f"{interaction.user.mention}のデータがないため、そもそも与える経験値がありません\n喋ろう!!!!", silent=True)
            return
        elif not targetdb:
            newdb = User(userid=target.id, username=target.name)
            session.add(newdb)
            session.commit()
            await interaction.response.send_message(f"{target.mention}のデータがなかったため、只今作成しました\nもう一度コマンドを実行して付与してください", silent=True)
            return
        givedb_allexp = (givedb.level * 10000) + givedb.exp
        if givedb_allexp < givexp:
            await interaction.response.send_message(f"コマ研レベルに借金機能はありません(笑)\n所持経験値量：{givedb_allexp} < 付与予定経験値量：{givexp}", silent=True)
            return

        givedb.exp -= givexp
        givedb.allremoveexp += givexp
        while givedb.exp < 0:
            givedb.level -= 1
            givedb.exp += 10000
        targetdb.exp += givexp
        targetdb.alladdexp += givexp
        while targetdb.exp >= 10000:
            targetdb.level += 1
            targetdb.exp -= 10000
        givedb.dailygivexp = True
        session.commit()
        await interaction.response.send_message(f"{target.mention}に{givexp}与えました", silent=True)

    @app_commands.command(name="csetleveling", description="【運営用】参加者のLv/exp変更)")
    @app_commands.describe(choice="選択肢", target="変更する人", level="レベル", experience="経験値")
    @app_commands.choices(
        choice=[
            app_commands.Choice(value="add", name="加算"),
            app_commands.Choice(value="remove", name="減算"),
            app_commands.Choice(value="set", name="設定"),
            app_commands.Choice(value="stop", name="権限停止")
        ]
    )
    async def setleveling(self, interaction: discord.Interaction, choice: app_commands.Choice[str], target: discord.Member, level: int = 0, experience: int = 0):
        setuserdb = session.query(User).filter_by(userid=target.id).first()

        if interaction.guild.get_role(config.administrater_role_id) not in interaction.user.roles:
            await interaction.response.send_message("権限ないよ！", ephemeral=True)
            return
        if not setuserdb:
            newdb = User(userid=target.id, username=target.name)
            session.add(newdb)
            session.commit()
            await interaction.response.send_message(f"{target.mention}のデータベースがまだなかったため只今生成しました\nもう一度コマンドを実行してください")
            return
        if level == 0 and experience == 0 and choice.value != "stop":
            await interaction.response.send_message("`level`または`experience`またはその両方に引数がありません\nどちらか一つは引数を指定してください")
            return

        match choice.value:
            case "add":
                setuserdb.exp += experience
                setuserdb.level += level
                setuserdb.alladdexp += (level * 10000) + experience
                while setuserdb.exp >= 10000:
                    setuserdb.level += 1
                    setuserdb.exp -= 10000
                session.commit()
                await interaction.response.send_message(f"{target.mention}に{level}Lv{experience}exp分を付与しました", silent=True)
            case "remove":
                if ((setuserdb.level * 10000) + setuserdb.exp) <= ((level * 10000) + experience):
                    setuserdb.exp = 0
                    setuserdb.level = 0
                    session.commit()
                else:
                    setuserdb.exp -= experience
                    setuserdb.level -= level
                    setuserdb.allremoveexp += (level * 10000) + experience
                    while setuserdb.exp < 0:
                        setuserdb.level -= 1
                        setuserdb.exp += 10000
                    session.commit()
                await interaction.response.send_message(f"{target.mention}の{level}Lv{experience}exp分をはく奪しました", silent=True)
            case "set":
                if experience >= 10000:
                    await interaction.response.send_message("`experience`が10000以上のため、設定できません")
                    return
                setuserdb.exp = experience
                setuserdb.level = level
                session.commit()
                await interaction.response.send_message(f"{target.mention}を{level}Lv{experience}expに設定しました", silent=True)
            case "stop":
                if setuserdb.noxp is False:
                    setuserdb.noxp = True
                    session.commit()
                    await interaction.response.send_message(f"{target.mention}のレベルシステムを無効化しました", silent=True)
                else:
                    setuserdb.noxp = False
                    session.commit()
                    await interaction.response.send_message(f"{target.mention}のレベルシステムを有効化しました", silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cmdbotlevelcom(bot))
