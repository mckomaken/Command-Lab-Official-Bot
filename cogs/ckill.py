import discord
from discord import Member, app_commands
from discord.ext import commands

import json
import random


def kill(name, target=None):

    # jsonファイル を dict(lang_data) に変換
    with open(file='./assets/ja_jp.json', mode='r', encoding='utf-8') as file:
        lang_data = json.load(file)

    # lang_data からデスログ、エンティティ名、アイテム名を抽出
    death_logs = [v for k, v in lang_data.items() if "death." in k]
    entities = [v.replace("のスポーンエッグ", "") for k, v in lang_data.items() if "item.minecraft." in k and "_spawn_egg" in k]
    items = [v for k, v in lang_data.items() if "item.minecraft." in k]

    # もしtargetがいなかったら、targetをエンティティの中から選出する
    if target is None:
        target = random.choice(entities)

    # キルログ生成
    death_log = random.choice(death_logs).replace("%1$s", name + " ").replace("%2$s", target).replace("%3$s", f"[{random.choice(items)}]")
    return death_log


class CKill(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ckill", description="キルコマンド(ネタ)")
    @app_commands.describe(target="キルするユーザー(任意)")
    async def ckill(self, interaction: discord.Interaction, target: str = None):
        await interaction.response.send_message(kill(interaction.user.mention, target))


async def setup(bot: commands.Bot):
    await bot.add_cog(CKill(bot))
