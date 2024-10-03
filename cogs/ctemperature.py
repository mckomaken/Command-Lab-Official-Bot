import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock


class CTemperature(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ctemperature", description="温度変換")
    @app_commands.describe(c="変換したい温度を℃単位で記入してください")
    async def ctemperature(self, interaction: discord.Interaction, c: float):
        K = c + 273.15
        F = 1.8 * c + 32
        emb = discord.Embed(
            title="温度変換結果", description=f"摂氏(℃){create_codeblock(c)}"
        )
        emb.add_field(name="華氏(℉)", value=create_codeblock(F))
        emb.add_field(name="ケルビン(K)", value=create_codeblock(K))

        await interaction.response.send_message(embed=emb)


async def setup(bot: commands.Bot):
    await bot.add_cog(CTemperature(bot))
