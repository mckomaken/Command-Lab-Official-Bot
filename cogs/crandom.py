from discord.ext import commands
import discord
from discord import app_commands
import random
import re


class CRandom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="crandom", description="マイクラの/randomコマンドの一部です(reset引数なし)")
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id))
    @app_commands.describe(
        mode="value : 自分にのみ表示・roll : 全員に公開",
        range="マイクラの書き方に則って範囲を書いてください"
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="roll", value="mroll"),
            app_commands.Choice(name="value", value="mvalue")
        ]
    )
    async def crandom(self, interaction: discord.Interaction, mode: app_commands.Choice[str], range: str):
        start = -2147483648
        end = 2147483647
        numlist = []
        pattern1 = r"[+-]?\d{1,}..[+-]?\d{1,}"
        pattern2 = r"[+-]?\d{1,}.."
        pattern3 = r"..[+-]?\d{1,}"
        numlist = re.findall(r'[+-]?\d+', range)

        if re.fullmatch(pattern1, range):
            starts = int(numlist[0])
            ends = int(numlist[1])
            if starts >= ends:
                await interaction.response.send_message("「[小さい数字]..[大きい数字]」って書いてね", ephemeral=True)
                return
            elif abs(starts - ends) + 1 > 2147483646:
                await interaction.response.send_message("範囲が広すぎます\n範囲の大きさは2以上2147483646以下です", ephemeral=True)
                return
            elif starts <= start:
                await interaction.response.send_message("[小さい数字]は-2147483648より大きい数で書いてね", ephemeral=True)
                return
            elif ends >= end:
                await interaction.response.send_message("[大きい数字]は2147483647より小さい数で書いてね", ephemeral=True)
                return
            num = random.randint(starts, ends)

        elif re.fullmatch(pattern2, range):
            starts = int(numlist[0])
            ends = end
            if abs(starts - ends) + 1 > 2147483646:
                await interaction.response.send_message("範囲が広すぎます\n範囲の大きさは2以上2147483646以下です", ephemeral=True)
                return
            elif starts <= start:
                await interaction.response.send_message("[小さい数字]は-2147483648より大きい数で書いてね", ephemeral=True)
                return
            elif starts >= ends:
                await interaction.response.send_message("[小さい数字]は2147483647より小さい数で書いてね", ephemeral=True)
                return
            num = random.randint(starts, end)

        elif re.fullmatch(pattern3, range):
            starts = start
            ends = int(numlist[0])
            if abs(start - ends) + 1 > 2147483646:
                await interaction.response.send_message("範囲が広すぎます\n範囲の大きさは2以上2147483646以下です", ephemeral=True)
                return
            elif ends >= end:
                await interaction.response.send_message("[大きい数字]は2147483647より小さい数で書いてね", ephemeral=True)
                return
            elif ends <= start:
                await interaction.response.send_message("[大きい数字]は-2147483648より大きい数で書いてね", ephemeral=True)
                return
            num = random.randint(start, ends)

        else:
            await interaction.response.send_message("範囲指定(range)が無効な記述です\n> ・1..10\n> ・..-10\n> ・1..\nのどれかで記述してください", ephemeral=True)
            return

        if mode.value == "mroll":
            await interaction.response.send_message(f"{interaction.user.display_name}は{num}を引きました ( 値の範囲は{starts}から{ends} )", ephemeral=False, silent=True)
        elif mode.value == "mvalue":
            await interaction.response.send_message(f"乱数 : {num}", ephemeral=True)

    # async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    #     if isinstance(error, app_commands.CommandOnCooldown):
    #         await interaction.response.send_message("クールダウン中です", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CRandom(bot))
