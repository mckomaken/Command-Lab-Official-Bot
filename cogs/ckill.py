from typing import Optional
import discord
from discord import Member, app_commands
from discord.ext import commands

import json
import random


class CKill(commands.Cog):
    lang_data: dict[str, str]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ckill", description="キルコマンド(ネタ)")
    @app_commands.describe(target="キルするユーザー(任意)")
    async def ckill(self, interaction: discord.Interaction, target: Optional[Member] = None):
        # もしtargetがいなかったら、targetをエンティティの中から選出する
        if target is None:
            target = random.choice(self.entities)

        # キルログ生成
        death_log = random.choice(self.death_logs) \
            .replace("%1$s", interaction.user.display_name + " ") \
            .replace("%2$s", target) \
            .replace("%3$s", f"[{random.choice(self.items)}]")

        await interaction.response.send_message(death_log)

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


async def setup(bot: commands.Bot):
    await bot.add_cog(CKill(bot))
