import base64

import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock


class CBase64(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            name="cbase64", description="Base64のエンコード/デコードを行います"
        )
        self.bot = bot

    @app_commands.command(
        name="encode", description="Base64のエンコードを行います"
    )
    @app_commands.guild_only()
    async def encode(self, interaction: discord.Interaction, text: str):
        embed = discord.Embed(
            color=0xFF99FF,
            title="Base64 Encode",
            description=create_codeblock(
                base64.b64encode(text.encode()).decode()
            )
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="decode", description="Base64のデコードを行います"
    )
    @app_commands.guild_only()
    async def decode(self, interaction: discord.Interaction, text: str):
        embed = discord.Embed(
            color=0xFF99FF,
            title="Base64 Decode",
            description=create_codeblock(
                base64.b64decode(text.encode()).decode()
            )
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    bot.tree.add_command(CBase64(bot=bot))
