from discord.ext import commands
from datetime import datetime, timedelta
from discord import ButtonStyle, app_commands
from database import User, session
import discord
from config.config import config

# bool1 : cog.cpresent.py使用中(プレゼント企画参加済みかどうか)


class LOttery(discord.ui.View):  # 抽選コマンド
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="応募", style=ButtonStyle.green, emoji="✅", custom_id="present")
    async def pressedLotteryButton(self, interaction: discord.Interaction, button: discord.ui.button):
        send_channel = await self.bot.fetch_channel(config.lottery_channel)
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
        if oubouser is None:
            userdb = User(userid=interaction.user.id, username=interaction.user.name)
            session.add(userdb)
            session.commit()
            await interaction.response.send_message("【応募条件】\n> 50チャット以上 または mcmd-level 3レベル以上\nのいずれかを満たしていません\n現時点でのチャット数: 0・レベル: 0\nサーバーでコマンドの質問や雑談をすればレベルが上がって行きます\nまた応募条件を満たした時にボタンを押しに来てください!!", ephemeral=True)
            return
        elif oubouser.noxp is True:
            await interaction.response.send_message("あなたには参加資格がありません", ephemeral=True)
            return
        elif oubouser.chatcount < 50 and oubouser.level < 3:
            await interaction.response.send_message(f"【応募条件】\n> 50チャット以上 または mcmd-level 3レベル以上\nのいずれかを満たしていません\n現時点でのチャット数: {oubouser.chatcount}・レベル: {oubouser.level}\nサーバーでコマンドの質問や雑談をすればレベルが上がって行きます\nまた応募条件を満たした時にボタンを押しに来てください!!", ephemeral=True)
            return
        elif oubouser.bool1 is True:
            await interaction.response.send_message("すでに応募済みです。抽選開始までお待ちください。", ephemeral=True)
            await send_channel.send(f"-# 〇２回以上押した人: <@{interaction.user.id}>")
            return
        else:
            await send_channel.send(f"応募者 : <@{interaction.user.id}> / {interaction.user.display_name}")
            oubouser.bool1 = True  # 応募済み
            oubouser.exp += 100  # 応募したら100経験値追加
            oubouser.alladdexp += 100
            if oubouser.exp >= 10000:
                oubouser.level += 1
                oubouser.exp -= 10000
            session.commit()
            await interaction.response.send_message("応募されました。抽選開始までお待ちください。", ephemeral=True)

    @discord.ui.button(label="企画終了", style=ButtonStyle.red, custom_id="delevent")
    async def pressedDeleventButton(self, interaction: discord.Interaction, button: discord.ui.button):
        role = interaction.guild.get_role(config.administrater_role_id)
        send_channel = await self.bot.fetch_channel(config.lottery_channel)
        if role in interaction.user.roles:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            await send_channel.send(f"-# ◆削除ボタン押した人: <@{interaction.user.id}>")


class CPresent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cpresent", description="【運営】present企画")
    @app_commands.describe(
        ptitle="〇周年プレゼント企画!/〇人プレゼント企画!/〇年-新年お年玉企画",
        kikann="応募期間(日数入力)",
        amagif1000="アマギフ1000円分をプレゼントする人数(初期値0)",
        amagif500="アマギフ500円分をプレゼントする人数(初期値0)",
        nitro="Nitro1ヶ月分をプレゼントする人数(初期値0)",
        abata_prof="DiscordShopで790円のものをプレゼントする人数(初期値0)",
        pripe="コンビニで買えるプリペイドカード系をプレゼントする人数(初期値0)",
        mcmd10000xp="mcmd-level 10000XPをプレゼントする人数(初期値0)",
        mcmd5000xp="mcmd-level 5000XPをプレゼントする人数(初期値0)",
        mcmd2500xp="mcmd-level 2500XPをプレゼントする人数(初期値0)",
        mcmd1000xp="mcmd-level 1000XPをプレゼントする人数(初期値0)",
    )
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cpresent(self, interaction: discord.Interaction, ptitle: str, kikann: int, amagif1000: int = 0, amagif500: int = 0, nitro: int = 0, abata_prof: int = 0, pripe: int = 0, mcmd10000xp: int = 0, mcmd5000xp: int = 0, mcmd2500xp: int = 0, mcmd1000xp: int = 0):

        syuuryoubi = datetime.now() + timedelta(days=kikann)
        fsyuuryoubi = syuuryoubi.strftime(" %Y/%m/%d ")
        tyuusennbi = syuuryoubi + timedelta(days=1)
        ftyuusennbi = tyuusennbi.strftime(" %Y/%m/%d ")

        str_amagif1000 = ""
        str_amagif500 = ""
        str_nitro = ""
        str_abata_prof = ""
        str_pripe = ""
        str_mcmd10000xp = ""
        str_mcmd5000xp = ""
        str_mcmd2500xp = ""
        str_mcmd1000xp = ""

        if amagif1000 > 0:
            str_amagif1000 = f"> `{amagif1000}名` : Amazonギフト券 1000円分\n"
        if amagif500 > 0:
            str_amagif500 = f"> `{amagif500}名` : Amazonギフト券 500円分\n"
        if nitro > 0:
            str_nitro = f"> `{nitro}名` : Discord Nitro 1ヶ月分\n"
        if abata_prof > 0:
            str_abata_prof = f"> `{abata_prof}名` : DiscordShop内790円商品\n"
        if pripe > 0:
            str_pripe = f"> `{pripe}名` : コンビニで買えるプリペイドカード系\n"
        if mcmd10000xp > 0:
            str_mcmd10000xp = f"> `{mcmd10000xp}名` : mcmd-level 10000XP\n"
        if mcmd5000xp > 0:
            str_mcmd5000xp = f"> `{mcmd5000xp}名` : mcmd-level 5000XP\n"
        if mcmd2500xp > 0:
            str_mcmd2500xp = f"> `{mcmd2500xp}名` : mcmd-level 2500XP\n"
        if mcmd1000xp > 0:
            str_mcmd1000xp = f"> `{mcmd1000xp}名` : mcmd-level 1000XP\n"

        PRESENT_DESCRIPTION = f"""
【応募条件】
1: このサーバーに抽選時に参加していること
2: 以下のいずれかを満たしていること
> ・コマ研レベル(mcmd-level)実装後 50チャット以上
> ・mcmd-level 3Lv以上
3: 下のボタンを押すこと
-# 4: 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw

【景品内容】
{str_amagif1000}{str_amagif500}{str_nitro}{str_abata_prof}{str_pripe}{str_mcmd10000xp}{str_mcmd5000xp}{str_mcmd2500xp}{str_mcmd1000xp}
【注意事項】
2アカウント以上の応募・ボタンの連打
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""
        present_embed = discord.Embed(
            title=ptitle,
            description=PRESENT_DESCRIPTION,
            color=0x2B9788,
            timestamp=datetime.now()
        )
        await interaction.response.send_message("送信しました", ephemeral=True)
        await interaction.channel.send(embed=present_embed)
        await interaction.channel.send(view=LOttery(self.bot))

    @app_commands.command(name="cpresent-reset", description="【運営】present企画-リセットコマンド")
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cpresentreset(self, interaction: discord.Interaction):
        results = session.query(User).all()
        for i in results:
            i.bool1 = False  # 応募済みをリセット
        session.commit()
        print("リセット完了")
        await interaction.response.send_message("リセットしました", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CPresent(bot))
    bot.add_view(LOttery(bot))
