import discord
from discord.ext import commands
from discord import app_commands

from utils.util import create_codeblock, create_embed


class CTemprature(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ctemprature", description="温度変換"
    )
    async def ctemprature(self, interaction: discord.Interaction, c: float):
        K = c - 293.15
        await interaction.response.send_message(
            embed=create_embed(
                title="温度変換結果",
                description=create_codeblock(K)
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CTemprature(bot))
