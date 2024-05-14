import discord
from discord import app_commands
from discord.ext import commands
from config.config import config
# self‐introduction
# CSelfintroduction


class CSelfintroduction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="cselfintroduction", description="自己紹介用コマンド"
    )
    @app_commands.describe(
        name="自分の名前(呼んで欲しい名前)",
        mcreki="マイクラ歴"
    )
    @app_commands.checks.has_role(
        config.administrater_role_id
    )
    async def selfin(
        self,
        interaction: discord.Interaction,
        title: str = None,
        description: str = None,
        sub_title: str = "",
        sub_description: str = ""
    ):
        await interaction.response.send_message(embed=discord.Embed(
            title="高校合格おめでとうございます!!", color=0x2b9788
        ))


async def setup(bot: commands.Bot):
    await bot.add_cog(CSelfintroduction(bot))
