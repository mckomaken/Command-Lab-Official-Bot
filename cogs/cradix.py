from typing import Optional

import discord
import numpy as np
from discord import app_commands
from discord.ext import commands


class CRadix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="cradix", description="入力した数値を2~16進数に変換します"
    )
    @app_commands.describe(
        num="進数変換したい数字を入れてください", mode="モードを選択してください(任意)"
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="2・4・8・10・16のみ表示します", value="cradix1"),
            app_commands.Choice(name="2~16進数を表示させます", value="cradix2"),
            app_commands.Choice(
                name="2~36進数を表示させます(17進数以降は自分のみの表示)",
                value="cradix3",
            ),
        ]
    )
    async def cradix(
        self, interaction: discord.Interaction, num: int, mode: Optional[str] = None
    ):
        absnum = abs(num)
        DESCRIPTION1 = f"""
```
|入力値| = {absnum}
2進数  : {np.base_repr(absnum, 2)}
4進数  : {np.base_repr(absnum, 4)}
8進数  : {np.base_repr(absnum, 8)}
10進数 : {np.base_repr(absnum, 10)}
16進数 : {np.base_repr(absnum, 16)}
```
Send by {interaction.user.mention}
"""
        DESCRIPTION2 = f"""
```
|入力値| = {absnum}
2進数  : {np.base_repr(absnum, 2)}
3進数  : {np.base_repr(absnum, 3)}
4進数  : {np.base_repr(absnum, 4)}
5進数  : {np.base_repr(absnum, 5)}
6進数  : {np.base_repr(absnum, 6)}
7進数  : {np.base_repr(absnum, 7)}
8進数  : {np.base_repr(absnum, 8)}
9進数  : {np.base_repr(absnum, 9)}
10進数 : {np.base_repr(absnum, 10)}
11進数 : {np.base_repr(absnum, 11)}
12進数 : {np.base_repr(absnum, 12)}
13進数 : {np.base_repr(absnum, 13)}
14進数 : {np.base_repr(absnum, 14)}
15進数 : {np.base_repr(absnum, 15)}
16進数 : {np.base_repr(absnum, 16)}
```
Send by {interaction.user.mention}
"""
        DESCRIPTION3 = f"""
```
|入力値| = {absnum}
17進数 : {np.base_repr(absnum, 17)}
18進数 : {np.base_repr(absnum, 18)}
19進数 : {np.base_repr(absnum, 19)}
20進数 : {np.base_repr(absnum, 20)}
21進数 : {np.base_repr(absnum, 21)}
22進数 : {np.base_repr(absnum, 22)}
23進数 : {np.base_repr(absnum, 23)}
24進数 : {np.base_repr(absnum, 24)}
25進数 : {np.base_repr(absnum, 25)}
26進数 : {np.base_repr(absnum, 26)}
27進数 : {np.base_repr(absnum, 27)}
28進数 : {np.base_repr(absnum, 28)}
29進数 : {np.base_repr(absnum, 29)}
30進数 : {np.base_repr(absnum, 30)}
31進数 : {np.base_repr(absnum, 31)}
32進数 : {np.base_repr(absnum, 32)}
33進数 : {np.base_repr(absnum, 33)}
34進数 : {np.base_repr(absnum, 34)}
35進数 : {np.base_repr(absnum, 35)}
36進数 : {np.base_repr(absnum, 36)}
```
Send by {interaction.user.mention}
"""
        radix_embed1 = discord.Embed(
            title="進数変換", description=DESCRIPTION1, color=0x58619A
        )

        radix_embed2 = discord.Embed(
            title="進数変換", description=DESCRIPTION2, color=0x58619A
        )

        radix_embed3 = discord.Embed(
            title="進数変換", description=DESCRIPTION3, color=0x58619A
        )

        if mode == "cradix2":
            await interaction.response.send_message(embed=radix_embed2)
        elif mode == "cradix3":
            await interaction.channel.send(embed=radix_embed2)
            await interaction.response.send_message(embed=radix_embed3, ephemeral=True)
        else:
            await interaction.response.send_message(embed=radix_embed1)


async def setup(bot: commands.Bot):
    await bot.add_cog(CRadix(bot))
