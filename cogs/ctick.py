from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_embed


class CTick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctick", description="tickに変換します")
    @app_commands.guild_only()
    async def ctick(
        self, interaction: discord.Interaction,
        year: Optional[int] = 0,
        month: Optional[int] = 0,
        week: Optional[int] = 0,
        day: Optional[int] = 0,
        hour: Optional[int] = 0,
        minute: Optional[int] = 0,
        second: Optional[int] = 0
    ):
        tick = 0
        tick += second * 20
        tick += minute * 60 * 20
        tick += hour * 60 * 60 * 20
        tick += day * 24 * 60 * 60 * 20
        tick += week * 7 * 24 * 60 * 60 * 20
        tick += month * 31 * 24 * 60 * 60 * 20
        tick += year * 12 * 31 * 24 * 60 * 60 * 20

        datestr = f"{year}年{month}ヶ月{week * 7 + day}日{hour}時間{minute}分{second}秒"

        await interaction.response.send_message(
            embed=create_embed(title="TICK換算", description=f"**{datestr}** は **{tick}Tick** です")
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CTick(bot))
