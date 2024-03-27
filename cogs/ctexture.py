import discord
import minecraft_data
from discord import app_commands
from discord.ext import commands


class CTexture(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="citem", description="アイテムを検索します"
    )
    @app_commands.describe(
        id="アイテムまたはブロックID"
    )
    @app_commands.guild_only()
    async def citem(self, interaction: discord.Interaction, id: str):
        mcd = minecraft_data(id)
        mcd.version


async def setup(bot: commands.Bot):
    await bot.add_cog(CTexture(bot))
