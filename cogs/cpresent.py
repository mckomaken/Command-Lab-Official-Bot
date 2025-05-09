from discord.ext import commands
from datetime import datetime, timedelta
from discord import ButtonStyle, app_commands

import discord


from config.config import config


class LOttery(discord.ui.View):  # 抽選コマンド
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="応募", style=ButtonStyle.green, emoji="✅", custom_id="present")
    async def pressedLotteryButton(self, interaction: discord.Interaction, button: discord.ui.button):
        send_channel = await self.bot.fetch_channel(config.lottery_channel)
        mee6role_5 = interaction.guild.get_role(config.mee6.five_5)
        if mee6role_5 not in interaction.user.roles:
            await interaction.response.send_message("MEE6レベルが5Lvになっていないため応募できません\nサーバーで雑談をしたり、コマンドの質問をすればレベルが上がって行きます\nまたMEE6レベルが5Lvになった時にボタンを押しに来てください！！", ephemeral=True)
        else:
            await send_channel.send(f"応募者 : <@{interaction.user.id}> / {interaction.user.display_name}")
            await interaction.response.send_message("応募されました。抽選開始までお待ちください。", ephemeral=True)

    @discord.ui.button(label="企画終了", style=ButtonStyle.red, custom_id="delevent")
    async def pressedDeleventButton(self, interaction: discord.Interaction, button: discord.ui.button):
        role = interaction.guild.get_role(config.administrater_role_id)
        send_channel = await self.bot.fetch_channel(config.lottery_channel)
        if role in interaction.user.roles:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            await send_channel.send(f"-# ◆削除ボタン押した人: <@{interaction.user.id}> / {interaction.user.id}")


class CPresent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cpresent", description="【運営】present企画")
    @app_commands.describe(
        choice="選択肢",
        daimei="○○プレゼント企画!(お年玉の時は適当に入力(表示されません))",
        tanni="単位(○○円・○○ヶ月)", ninnzuu="当選人数", kikann="応募期間(日数入力)"
    )
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="Nitro", value="pe1"),
            app_commands.Choice(name="アマゾンギフト券", value="pe2"),
            app_commands.Choice(name="アバターデコレーション", value="pe3"),
            app_commands.Choice(name="プロフィールエフェクト", value="pe4"),
            app_commands.Choice(name="お年玉企画", value="pe5"),
        ]
    )
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cpresent(self, interaction: discord.Interaction, choice: app_commands.Choice[str], daimei: str, ninnzuu: int, kikann: int, tanni: int = 0):

        syuuryoubi = datetime.now() + timedelta(days=kikann)
        fsyuuryoubi = syuuryoubi.strftime(" %Y/%m/%d ")
        tyuusennbi = syuuryoubi + timedelta(days=1)
        ftyuusennbi = tyuusennbi.strftime(" %Y/%m/%d ")

        NITRO_DESCRIPTION = f"""
### Discord Nitro {tanni}ヶ月分を{ninnzuu}名にプレゼント
【参加条件】
このサーバーに参加していること・下のボタンを押すこと
出来ればサーバーブーストはコマ研でやってね
-# 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw
【注意事項】
2回以上の応募/企画終了ボタンのクリック(タップ)・2アカウント以上の応募
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""

        AMAGIHU_DESCRIPTION = f"""
### アマゾンギフト券 {tanni}円分を{ninnzuu}名にプレゼント
【参加条件】
このサーバーに参加していること・下のボタンを押すこと
-# 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw
【注意事項】
2回以上の応募/企画終了ボタンのクリック(タップ)・2アカウント以上の応募
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""

        ABATADEKO_DESCRIPTION = f"""
### アバターデコレーションを{ninnzuu}名にプレゼント
【参加条件】
このサーバーに参加していること・下のボタンを押すこと
-# 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw
【注意事項】
2回以上の応募/企画終了ボタンのクリック(タップ)・2アカウント以上の応募
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""

        PROFEFFECT_DESCRIPTION = f"""
### プロフィールエフェクトを{ninnzuu}名にプレゼント
【参加条件】
このサーバーに参加していること・下のボタンを押すこと
-# 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw
【注意事項】
2回以上の応募/企画終了ボタンのクリック(タップ)・2アカウント以上の応募
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""

        OTOSIDAMA_DESCRIPTION = f"""
### Amazonギフト券500円分を{ninnzuu}名にプレゼント
【参加条件】
このサーバーに参加していること・下のボタンを押すこと
-# 春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)してくれたらうれしいけどw
【注意事項】
2回以上の応募/企画終了ボタンのクリック(タップ)・2アカウント以上の応募
→その回の全アカウントでの応募権はく奪
-# あまりにひどい/しつこい場合は今後一切の参加を認めない場合があります

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 00:00からVCにて発表
"""

        if choice.value == "pe1":
            if tanni == 0:
                await interaction.response.send_message("tanni引数入れ忘れてるよ!\n[Discord Nitro {tanni}ヶ月分を{ninnzuu}名にプレゼント]", ephemeral=True)
            else:
                nitro_embed = discord.Embed(
                    title=f"{daimei}プレゼント企画!!",
                    description=NITRO_DESCRIPTION,
                    color=0x2B9788,
                    timestamp=datetime.now()
                )
                await interaction.response.send_message("送信しました", ephemeral=True)
                await interaction.channel.send(embed=nitro_embed)
                await interaction.channel.send(view=LOttery(self.bot))

        elif choice.value == "pe2":
            if tanni == 0:
                await interaction.response.send_message("tanni引数入れ忘れてるよ!\n[アマゾンギフト券 {tanni}円分を{ninnzuu}名にプレゼント]", ephemeral=True)
            else:
                amagihu_embed = discord.Embed(
                    title=f"{daimei}プレゼント企画!!",
                    description=AMAGIHU_DESCRIPTION,
                    color=0x2B9788,
                    timestamp=datetime.now()
                )
                await interaction.response.send_message("送信しました", ephemeral=True)
                await interaction.channel.send(embed=amagihu_embed)
                await interaction.channel.send(view=LOttery(self.bot))

        elif choice.value == "pe3":
            abatadeko_embed = discord.Embed(
                title=f"{daimei}プレゼント企画!!",
                description=ABATADEKO_DESCRIPTION,
                color=0x2B9788,
                timestamp=datetime.now()
            )
            await interaction.response.send_message("送信しました", ephemeral=True)
            await interaction.channel.send(embed=abatadeko_embed)
            await interaction.channel.send(view=LOttery(self.bot))

        elif choice.value == "pe4":
            profeffect_embed = discord.Embed(
                title=f"{daimei}プレゼント企画!!",
                description=PROFEFFECT_DESCRIPTION,
                color=0x2B9788,
                timestamp=datetime.now()
            )
            await interaction.response.send_message("送信しました", ephemeral=True)
            await interaction.channel.send(embed=profeffect_embed)
            await interaction.channel.send(view=LOttery(self.bot))

        elif choice.value == "pe5":
            otosidama_embed = discord.Embed(
                title=f"{datetime.now().year}年-新年お年玉企画",
                description=OTOSIDAMA_DESCRIPTION,
                color=0x2B9788,
                timestamp=datetime.now()
            )
            await interaction.response.send_message("送信しました", ephemeral=True)
            await interaction.channel.send(embed=otosidama_embed)
            await interaction.channel.send(view=LOttery(self.bot))


async def setup(bot: commands.Bot):
    await bot.add_cog(CPresent(bot))
    bot.add_view(LOttery(bot))
