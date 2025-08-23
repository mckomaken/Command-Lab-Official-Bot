import json
import os
from datetime import datetime
from typing import Any, Optional

import aiofiles
import discord
from discord import Embed, app_commands
from discord.ext import commands

from schemas.data import CommandEntry
from utils.util import create_codeblock, create_embed


class CCommandInfoButtons(discord.ui.View):
    def __init__(self, je: Optional[Embed] = None, be: Optional[Embed] = None):
        super().__init__(timeout=None)
        if je is None:
            self.je.disabled = True
        if be is None:
            self.be.disabled = True
        self.je_embed = je
        self.be_embed = be

    @discord.ui.button(label="JE")
    async def je(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.je_embed)

    @discord.ui.button(label="BE")
    async def be(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.be_embed)


class CCommandInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ccommand", description="コマンドの情報を表示します")
    async def ccommand(self, interaction: discord.Interaction, command: str):
        async with aiofiles.open(
            os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb"
        ) as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]
            if command not in data:
                await interaction.response.send_message(
                    embed=create_embed(title="エラー", description="コマンドが不明です")
                )
                return
            d = CommandEntry.model_validate(data[command])

        je_embed = None
        be_embed = None
        if d.ver.je is not None:
            je_embed = Embed(
                color=0xAA00BB,
                title=f"/{command}",
                description=d.desc,
                timestamp=datetime.now(),
            )
            je_embed.set_author(name="Java Edition")
            je_embed.add_field(
                name="使用法",
                value=create_codeblock(
                    "/" + d.options.je if d.options.je != "-" else f"/{command}"
                ),
                inline=False,
            )
            je_embed.add_field(
                name="例",
                value=create_codeblock(
                    d.exmp.je if d.exmp.je != "-" else f"/{command}"
                ),
                inline=False,
            )

        if d.ver.be is not None:
            be_embed = Embed(
                color=0xAA00BB,
                title=f"/{command}",
                description=d.desc,
                timestamp=datetime.now(),
            )
            be_embed.set_author(name="Bedrock Edition")
            be_embed.add_field(
                name="使用法",
                value=create_codeblock(
                    "/" + d.options.be if d.options.be != "-" else f"/{command}"
                ),
                inline=False,
            )
            be_embed.add_field(
                name="例",
                value=create_codeblock(
                    d.exmp.be if d.exmp.be != "-" else f"/{command}"
                ),
                inline=False,
            )

        view = None
        if d.is_diff:
            view = CCommandInfoButtons(je_embed, be_embed)

        await interaction.response.send_message(embed=(je_embed or be_embed), view=view)

    @ccommand.autocomplete("command")
    async def ccommand_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        async with aiofiles.open(
            os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb"
        ) as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]

            return [
                app_commands.Choice(name=k, value=k)
                for k in data.keys()
                if k.startswith(current)
            ][:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(CCommandInfo(bot))
