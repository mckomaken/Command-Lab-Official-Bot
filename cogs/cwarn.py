import discord
from discord import app_commands
from discord.ext import commands
from database import User, session
from config.config import config


class Cwarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cwarn", description="【運営用】参加者の警告設定")
    @app_commands.describe(choice="選択肢", target="警告する人", reason="理由", number="違反番号(1~5)")
    @app_commands.choices(
        choice=[
            app_commands.Choice(value="add", name="加点(理由引数必須)"),
            app_commands.Choice(value="remove", name="減点(指定番号の違反を削除)"),
            app_commands.Choice(value="edit", name="編集(指定番号の違反を編集/変更前に一覧で確認してください)"),
            app_commands.Choice(value="list", name="一覧表示")
        ]
    )
    async def cwarn(self, interaction: discord.Interaction, choice: app_commands.Choice[str], target: discord.Member, reason: str = "", number: int = 0):
        warnuserdb = session.query(User).filter_by(userid=target.id).first()

        if interaction.guild.get_role(config.administrater_role_id) not in interaction.user.roles:
            await interaction.response.send_message("権限ないよ！", ephemeral=True)
            return
        if not warnuserdb:
            newdb = User(userid=target.id, username=target.name)
            session.add(newdb)
            session.commit()
            await interaction.response.send_message(f"{target.mention}のデータベースがまだなかったため只今生成しました\nもう一度コマンドを実行してください", silent=True)
            return

        match choice.value:
            case "add":
                warnuserdb.warnpt += 1
                if warnuserdb.warnreason1 is None or warnuserdb.warnreason1 == "":
                    warnuserdb.warnreason1 = reason
                    num = 1
                elif warnuserdb.warnreason2 is None or warnuserdb.warnreason2 == "":
                    warnuserdb.warnreason2 = reason
                    num = 2
                elif warnuserdb.warnreason3 is None or warnuserdb.warnreason3 == "":
                    warnuserdb.warnreason3 = reason
                    num = 3
                elif warnuserdb.warnreason4 is None or warnuserdb.warnreason4 == "":
                    warnuserdb.warnreason4 = reason
                    num = 4
                else:
                    warnuserdb.warnreason5 = reason
                    num = 5
                session.commit()
                await interaction.response.send_message(f"{target.mention}に違反点数を追加しました\nNo.{num}・理由:{reason}", silent=True)

            case "remove":
                if number <= 0 or number > 5:
                    await interaction.response.send_message("`number`が指定されていません。違反番号(1~5)を指定してください", ephemeral=True)
                    return
                warnuserdb.warnpt -= 1
                match number:
                    case 1:
                        warnuserdb.warnreason1 = ""
                    case 2:
                        warnuserdb.warnreason2 = ""
                    case 3:
                        warnuserdb.warnreason3 = ""
                    case 4:
                        warnuserdb.warnreason4 = ""
                    case 5:
                        warnuserdb.warnreason5 = ""
                session.commit()
                await interaction.response.send_message(f"{target.mention}のNo.{number}の違反を削除しました\nNo.{number}・理由:{reason}", silent=True)

            case "edit":
                if number <= 0 or number > 5:
                    await interaction.response.send_message("`number`が指定されていません。違反番号(1~5)を指定してください", ephemeral=True)
                    return
                match number:
                    case 1:
                        oldreason = warnuserdb.warnreason1
                        warnuserdb.warnreason1 = reason
                    case 2:
                        oldreason = warnuserdb.warnreason2
                        warnuserdb.warnreason2 = reason
                    case 3:
                        oldreason = warnuserdb.warnreason3
                        warnuserdb.warnreason3 = reason
                    case 4:
                        oldreason = warnuserdb.warnreason4
                        warnuserdb.warnreason4 = reason
                    case 5:
                        oldreason = warnuserdb.warnreason5
                        warnuserdb.warnreason5 = reason
                session.commit()
                await interaction.response.send_message(f"{target.mention}のNo.{number}の違反を編集しました\nNo.{number}・旧理由:{oldreason}\n↓\nNo.{number}・新理由:{reason}", silent=True)
            case "list":
                warnlistembed = discord.Embed(
                    title=f"{target.display_name}の違反一覧",
                    description=f"## 合計違反点数 : {warnuserdb.warnpt}\n```\nNo1 : {warnuserdb.warnreason1}\nNo2 : {warnuserdb.warnreason2}\nNo3 : {warnuserdb.warnreason3}\nNo4 : {warnuserdb.warnreason4}\nNo5 : {warnuserdb.warnreason5}\n```",
                    color=0xFF0000,
                )
                await interaction.response.send_message(embed=warnlistembed, silent=True)

    @app_commands.command(name="cwarn-list", description="自分の警告状況確認コマンド")
    async def cwarnlist(self, interaction: discord.Interaction):
        warnuserdb = session.query(User).filter_by(userid=interaction.user.id).first()
        if not warnuserdb:
            await interaction.response.send_message("あなたはまだ警告を受けていません", ephemeral=True)
            return
        warnlistembed = discord.Embed(
            title=f"{interaction.user.display_name}の違反一覧",
            description=f"## 合計違反点数 : {warnuserdb.warnpt}\n```\nNo1 : {warnuserdb.warnreason1}\nNo2 : {warnuserdb.warnreason2}\nNo3 : {warnuserdb.warnreason3}\nNo4 : {warnuserdb.warnreason4}\nNo5 : {warnuserdb.warnreason5}\n```",
            color=0xFF0000,
        )
        await interaction.response.send_message(embed=warnlistembed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cwarn(bot))
