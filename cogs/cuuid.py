import uuid
from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock

MESSAGE = """
-----------------------------------------------------
{}個のUUIDを自動生成しました
BEのAdd-on制作にお役立てください
-----------------------------------------------------
"""


class CUUIDCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="cuuid", description="UUIDを生成します"
    )
    @app_commands.describe(
        count="生成する量(デフォルト: 2)"
    )
    async def cuuid(
        self, interaction: discord.Interaction,
        count: Optional[app_commands.Range[int, 1, 25]] = 2
    ):
        uuJST_time = datetime.now()

        uuid_embed = discord.Embed(
            title="UUID Generator",
            description=MESSAGE.format(count),
            color=0x58619a,
            timestamp=uuJST_time
        )

        for i in range(count):
            uuid2 = str(uuid.uuid4())
            uuid2_nosep = uuid2.replace("-", "")

            uuid_embed.add_field(name=f"{i + 1}個目", value=f"{create_codeblock(uuid2)}{create_codeblock(uuid2_nosep)}", inline=False)

        await interaction.response.send_message(embed=uuid_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CUUIDCog(bot))
