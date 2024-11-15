import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from app_commands import Range


class CRadix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cradix", description="指定された数値を別の基数に変換します")
    @app_commands.describe(
        value="変換する数値(例: 10, 0x10, 0b10 など)",
        target_base="変換先の基数(2以上の整数)"
    )
    async def cradix(
        self,
        interaction: discord.Interaction,
        value: str,
        target_base: Range[int, 2]
    ):
        try:
            # 入力値をintとして解釈
            original_value = int(value, 0)
            # n進数に変換
            converted_value = f"{original_value:b}" if target_base == 2 else f"{original_value:x}" if target_base == 16 else format(original_value, f"0{target_base}")
        except ValueError:
            error_embed = discord.Embed(
                color=0xFF0000,
                title="エラー",
                description=f"指定された値 '{value}' を整数として解釈できませんでした。",
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        embed = discord.Embed(
            color=0x58619A,
            title="基数変換",
            description=f"`{value}`(10進数: {original_value}) = {target_base}進数: {converted_value}",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CRadix(bot))
