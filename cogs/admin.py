from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from config.config import config

TITLES = [
    "【お知らせ】",
    "再起動を行います",
    "使用停止期間",
    "荒らし対応中",
    "既知のバグについて",
    "アプデ対応中",
    "HP公開中!!!!!",
]

DESCRIPTIONS = [
    "すぐ復活するはず(笑)",
    "ちょっと長めの再起動になります",
    "`2024/xx/yy-hh:mm`頃～`2024/xx/yy-hh:mm`頃まで\n実家帰省のためBotが止まります",
    "# **__リンクは絶対に踏まないでください__**",
    "https://komaken.net/\n検索してね(^^♪",
    "# v2.xにアップデートされました",
]

LOTTERY_DESCRIPTION = """
### Discord Nitro 1ヶ月分を1名にプレゼント
参加条件 : このサーバーに参加していること・下のボタンを押すこと
任意条件 : サーバーブーストは出来ればコマ研にやってね
           春菊のチャンネルとうろk((((殴殴
-# 冗談です(笑)
注意事項 : ３回以上押した場合は無効になります

締め切り : 10/25 23:59"
当選発表 : 10/26 00:00からVCにて発表
"""


class CNoticeConfirm(discord.ui.View):
    def __init__(self, embed: discord.Embed):
        super().__init__(timeout=None)
        self.embed = embed

    @discord.ui.button(label="OK")
    async def ok(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(
            content="送信しました", view=None, embed=None
        )
        await interaction.channel.send(embed=self.embed)


class LOttery(discord.ui.View):  # 抽選コマンド
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="応募")
    async def pressedLotteryButton(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        send_channel = await self.bot.fetch_channel(config.lottery_channel)
        await send_channel.send(
            f"応募者 : {interaction.user.display_name}\n```{interaction.user.name}```"
        )
        await interaction.response.send_message(
            "応募されました。抽選開始までお待ちください。", ephemeral=True
        )


class CAdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cmisc", description="【運営】運営専用雑コマンド")
    @app_commands.describe(choice="選択肢")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="高校おめ", value="cl1"),
            app_commands.Choice(name="大学おめ", value="cl2"),
            app_commands.Choice(name="プレゼント企画", value="cl3"),
        ]
    )
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cmisc(
        self, interaction: discord.Interaction, choice: app_commands.Choice[str]
    ):
        if choice.value == "cl1":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="高校合格おめでとうございます!!", color=0x2B9788
                )
            )
        elif choice.value == "cl2":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="大学合格おめでとうございます!!", color=0x2B9788
                )
            )
        elif choice.value == "cl3":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="1500人到達プレゼント企画!!",
                    description=LOTTERY_DESCRIPTION,
                    color=0x2B9788,
                ),
                view=LOttery(self.bot),
            )

    @app_commands.command(name="cn", description="【運営】各種お知らせ用")
    @app_commands.describe(
        title="タイトル",
        description="説明",
        sub_title="サブタイトル",
        sub_description="サブ説明",
    )
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cn(
        self,
        interaction: discord.Interaction,
        title: str = None,
        description: str = None,
        sub_title: str = "",
        sub_description: str = "",
    ):
        mntJST_time = datetime.now()
        if title is not None:
            title = title.replace("\\n", "\n")

        if description is not None:
            description = description.replace("\\n", "\n")

        notice_embed = discord.Embed(
            title=title, description=description, color=0xFF580F, timestamp=mntJST_time
        )

        notice_embed.set_footer(text=f"Send by {interaction.user.display_name}")

        if sub_title != "" and sub_description != "":
            notice_embed.add_field(
                name=sub_title,
                value=sub_description,
            )

        await interaction.response.send_message(
            content="本当にこの内容で送信していいんか?",
            embed=notice_embed,
            ephemeral=True,
            view=CNoticeConfirm(embed=notice_embed),
        )

    @cn.autocomplete("title")
    async def cn_title(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=n, value=n) for n in TITLES]

    @cn.autocomplete("description")
    async def cn_description(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=n, value=n) for n in DESCRIPTIONS]


async def setup(bot: commands.Bot):
    await bot.add_cog(CAdminCog(bot))
