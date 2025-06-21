import io
import random
import struct
import zlib

import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock, create_embed


class CDice(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="cdice")
        self.bot = bot

    @app_commands.command(name="roll", description="ダイスを振ります")
    @app_commands.checks.cooldown(1, 3)
    async def roll(self, interaction: discord.Interaction, dices: int, upto: int):
        try:
            total = 0
            if dices > 100 or upto > 10000 or dices < 1 or upto < 1:
                raise ValueError
            rolls = [random.randint(1, upto) for _ in range(dices)]
        except ValueError:
            await interaction.response.send_message(
                embed=create_embed("エラー", "値が無効です（ダイスの数：1～100、出目：1～10000）"), ephemeral=True
            )

        rolls_concatenated = ",".join([str(i) for i in rolls])
        total += sum(rolls)

        embed = discord.Embed()

        embed.color = 0x808080
        if dices == 1:
            embed.description = f"結果: {total}"
        else:
            embed.description = f"結果: {rolls_concatenated} -> {total}"

        await interaction.response.send_message(embed=embed, silent=True)

    @app_commands.command(name="try", description="ダイスを振り、合計が値以下で成功と判定します")
    @app_commands.checks.cooldown(1, 3)
    async def trying(self, interaction: discord.Interaction, dices: int, upto: int, value: int):
        try:
            total = 0
            if dices > 100 or upto > 10000 or dices < 1 or upto < 1:
                raise ValueError
            rolls = [random.randint(1, upto) for _ in range(dices)]
        except ValueError:
            await interaction.response.send_message(
                embed=create_embed("エラー", "値が無効です（ダイスの数：1～100、出目：1～10000）"), ephemeral=True
            )

        rolls_concatenated = ",".join([str(i) for i in rolls])
        total += sum(rolls)

        embed = discord.Embed()

        if dices == 1:
            if total <= value:
                embed.color = 0x456cba
                embed.description = f"結果: {total} <= {value} 成功！"
            else:
                embed.color = 0xba4545
                embed.description = f"結果: {total} > {value} 失敗"
        else:
            if total <= value:
                embed.color = 0x456cba
                embed.description = f"結果: {rolls_concatenated} -> {total} <= {value} 成功！"
            else:
                embed.color = 0xba4545
                embed.description = f"結果: {rolls_concatenated} -> {total} > {value} 失敗"

        await interaction.response.send_message(embed=embed, silent=True)

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
       if isinstance(error, app_commands.CommandOnCooldown):
           await interaction.response.send_message("ちょっと待って！", ephemeral=True)


async def setup(bot: commands.Bot):
    bot.tree.add_command(CDice(bot))
