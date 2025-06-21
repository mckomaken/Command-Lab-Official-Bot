from typing import Optional
import discord
from discord import Member, app_commands
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions

import json
import random


def escape(text: str) -> str:
    return escape_markdown(escape_mentions(text), as_needed=True)


class CKill(commands.Cog):
    lang_data: dict[str, str]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # 最大数設定
        self.max_count = 5

    def generate_death_log(self, victim: Optional[str], player: str) -> str:
        death_logs = self.death_logs

        # 指定なし -> 1人のみのdeath log
        if victim is None:
            death_logs = [t for t in self.death_logs if "%2$s" not in t]
            victim = ""
        else:
            victim, player = player, victim

        # キルログ生成
        return random.choice(death_logs) \
            .replace("%1$s", escape(player)) \
            .replace("%2$s", escape(victim)) \
            .replace("%3$s", f"[{random.choice(self.items)}]")

    @app_commands.command(name="ckill", description="キルコマンド(ネタ)")
    @app_commands.describe(target="キルするユーザー(任意)", count="回数(デフォルト1)")
    @app_commands.checks.cooldown(1, 3)
    async def ckill(
        self, interaction: discord.Interaction,
        target: Optional[Member] = None,
        count: Optional[int] = 1
    ):
        target_name = None
        if target:
            target_name = escape(target.display_name)

        # 最大数制限
        if 0 < count <= self.max_count:
            logs: list[str] = []
            for _ in range(count):
                logs.append(self.generate_death_log(
                    target_name,
                    escape(interaction.user.display_name)
                ))

            await interaction.response.send_message(
                "\n".join(logs).rstrip("\n"),
                allowed_mentions=discord.AllowedMentions.none()
            )
        else:
            await interaction.response.send_message(
                f"countには{self.max_count}以下の自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪",
                ephemeral=True
            )

    async def cog_load(self) -> None:
        # jsonファイル を dict(lang_data) に変換
        with open(file='./assets/ja_jp.json', mode='r', encoding='utf-8') as file:
            self.lang_data = json.load(file)

            self.death_logs = [v for k, v in self.lang_data.items() if "death." in k]
            self.entities = [
                v.replace("のスポーンエッグ", "") for k, v in self.lang_data.items()
                if "item.minecraft." in k and "_spawn_egg" in k
            ]
            self.items = [v for k, v in self.lang_data.items() if "item.minecraft." in k]

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
       if isinstance(error, app_commands.CommandOnCooldown):
           await interaction.response.send_message("ちょっと待って！", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CKill(bot))
