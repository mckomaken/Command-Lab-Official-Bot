import discord

from datetime import datetime
from discord import app_commands
from discord.ext import commands

HELP_MESSAGE = """
/chelp : この説明文が出てきます
/cping : サーバーとBotとのping値を測定できます
/cuuid : 2個のUUIDを自動生成してくれます
/cpack-mcmeta : ResourcePackとDataPackのpack_formatの番号一覧を表示します"
"""


class CHelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chelp", description="このBotができること一覧")
    @app_commands.guild_only()
    async def chelp(self, interaction: discord.Interaction):

        chJST_time = datetime.now()

        chelp_embed = discord.Embed(
            title="コマンド一覧",
            description=HELP_MESSAGE,
            color=0x2b9900,
            timestamp=chJST_time
        )

        await interaction.response.send_message(embed=chelp_embed)

    @app_commands.command(name="cping", description="pingを計測します")
    @app_commands.guild_only()
    async def cping(self, interaction: discord.Interaction):

        piJST_time = datetime.now()
        text = f'{round(self.bot.latency*1000)}ms'

        ping_embed = discord.Embed(
            title="現在のping",
            description=text,
            timestamp=piJST_time
        )

        await interaction.response.send_message(embed=ping_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CHelpCog(bot))
