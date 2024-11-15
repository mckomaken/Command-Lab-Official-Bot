from discord.ext import commands
import discord
from discord import app_commands
import numpy as np


class CRadix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cradix", description="入力した数値を2~16進数に変換します")
    @app_commands.describe(num="進数変換したい数字を入れてください")
    async def cybase64(self, interaction: discord.Interaction, num: int):
        absnum = abs(num)
        DESCRIPTION = f"""
|入力値| = {absnum}
2進数 : {np.base_repr(absnum, 2)}
3進数 : {np.base_repr(absnum, 3)}
4進数 : {np.base_repr(absnum, 4)}
5進数 : {np.base_repr(absnum, 5)}
6進数 : {np.base_repr(absnum, 6)}
7進数 : {np.base_repr(absnum, 7)}
8進数 : {np.base_repr(absnum, 8)}
9進数 : {np.base_repr(absnum, 9)}
10進数 : {np.base_repr(absnum, 10)}
11進数 : {np.base_repr(absnum, 11)}
12進数 : {np.base_repr(absnum, 12)}
13進数 : {np.base_repr(absnum, 13)}
14進数 : {np.base_repr(absnum, 14)}
15進数 : {np.base_repr(absnum, 15)}
16進数 : {np.base_repr(absnum, 16)}
"""
        radix_embed = discord.Embed(
            title="進数変換",
            description=DESCRIPTION,
            color=0x58619A
        )
        await interaction.response.send_message(embed=radix_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CRadix(bot))
