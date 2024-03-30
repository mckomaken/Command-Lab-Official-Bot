import discord
from discord.ext import commands
from discord import app_commands

from utils.util import create_codeblock


class CTemperature(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ctemperature", description="温度変換"
    )
    async def ctemperature(self, interaction: discord.Interaction, c: float):
        K = c - 293.15
        F = 1.8 * c + 32
        emb = discord.Embed(
            title="温度変換結果",
            description=f"摂氏{create_codeblock(c)}"
        )
        emb.add_field(name="華氏", value=create_codeblock(F))
        emb.add_field(name="ケルビン", value=create_codeblock(K))

        await interaction.response.send_message(
            embed=emb
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CTemperature(bot))
