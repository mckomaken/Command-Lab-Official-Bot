import io
import discord

from typing import Optional
from discord.ext import commands
from discord import app_commands
from pydantic import BaseModel
from datetime import datetime

from config import PackVersionEntry, pack_versions
from table2ascii import table2ascii, Alignment, PresetStyle

from util import create_codeblock

VERSION_NOT_FOUND = discord.Embed(
    title="エラー", description="バージョンが見つかりません。", color=0xff0000
)


class PackMcmetaV(BaseModel):
    pack_format: int
    description: str


class PackMcmeta(BaseModel):
    pack: PackMcmetaV


@app_commands.guild_only()
class CPackMcMeta(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="cpack-mcmeta")
        self.bot = bot

    # ----------------------------------------------------------------

    @app_commands.command(
        name="datapacks",
        description="データパックのpack_formatをすべて出力します"
    )
    @app_commands.guild_only()
    async def datapacks(
        self, interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="データパックバージョン一覧",
            description=create_codeblock(
                table2ascii(
                    header=["Version", "Format"],
                    body=[(k, v.dp) for k, v in pack_versions.versions.items() if v.dp != -1],
                    style=PresetStyle.thin_box,
                    alignments=Alignment.LEFT
                )
            )
        )

        await interaction.response.send_message(embed=embed)

    # ----------------------------------------------------------------

    @app_commands.command(
        name="resourcepacks",
        description="リソースパックのpack_formatをすべて出力します"
    )
    @app_commands.guild_only()
    async def resourcepacks(
        self, interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="リソースパックバージョン一覧",
            description=create_codeblock(
                table2ascii(
                    header=["Version", "Format"],
                    body=[(k, v.rp) for k, v in pack_versions.versions.items()],
                    style=PresetStyle.thin_box,
                    alignments=Alignment.LEFT
                )
            )
        )

        await interaction.response.send_message(embed=embed)

    # ----------------------------------------------------------------

    @app_commands.command(
        name="search",
        description="pack_formatを検索します"
    )
    @app_commands.guild_only()
    async def search(
        self, interaction: discord.Interaction, version: str
    ):
        ver = [int(n) for n in version.split(".")]
        if len(ver) == 2:
            ver[2] = 0

        embed = discord.Embed(
            title="pack_formatバージョン検索", description=version
        )

        for k, v in pack_versions.versions.items():
            if "-" in k:
                ver0 = [int(n) for n in k.split("-")[0].split(".")]
                ver1 = [int(n) for n in k.split("-")[1].split(".")]

                if ver0[1] <= ver[1] <= ver1[1] and ver0[2] <= ver[2] <= ver1[2]:
                    embed.add_field(name="リソースパックバージョン", value=f"```{v.rp}```")
                    embed.add_field(name="データパックバージョン", value=f"```{v.dp}```")
                    await interaction.response.send_message(embed=embed)

                    return
            else:
                if version == k:
                    embed.add_field(name="リソースパックバージョン", value=f"```{v.rp}```")
                    embed.add_field(name="データパックバージョン", value=f"```{v.dp}```")
                    await interaction.response.send_message(embed=embed)

                    return

        await interaction.response.send_message(embed=VERSION_NOT_FOUND)

    def _search(self, version: str) -> Optional[PackVersionEntry]:
        ver = [int(n) for n in version.split(".")]
        if len(ver) == 2:
            ver[2] = 0

        if len(ver) != 3:
            return None

        for k, v in pack_versions.versions.items():
            if "-" in k:
                ver0 = [int(n) for n in k.split("-")[0].split(".")]
                ver1 = [int(n) for n in k.split("-")[1].split(".")]

                if ver0[1] <= ver[1] <= ver1[1] and ver0[2] <= ver[2] <= ver1[2]:
                    return v
            else:
                if version == k:
                    return v

    @app_commands.command(name="generate-dp", description="データパックのpack.mcmetaを生成します")
    @app_commands.guild_only()
    async def generate_dp(self, interaction: discord.Interaction, description: str, version: str):
        ver: PackVersionEntry = self._search(version)
        if ver is None:
            await interaction.response.send_message(embed=VERSION_NOT_FOUND)
            return

        embed = discord.Embed(
            color=0x89C4FF,
            title="pack.mcmeta Generator",
            description="生成完了!",
            timestamp=datetime.now()
        )
        embed.add_field(name="説明", value=create_codeblock(description))
        embed.add_field(name="パックバージョン", value=create_codeblock(f"({version}) {ver.dp}"))

        data: str = PackMcmeta(pack=PackMcmetaV(pack_format=ver.dp, description=description)).model_dump_json(indent=4)
        file = discord.File(io.StringIO(data), filename="pack.mcmeta")

        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)

    @app_commands.command(name="generate-rp", description="リソースパックのpack.mcmetaを生成します")
    @app_commands.guild_only()
    async def generate_rp(self, interaction: discord.Interaction, description: str, version: str):
        ver: PackVersionEntry = self._search(version)
        if ver is None:
            await interaction.response.send_message(embed=VERSION_NOT_FOUND)
            return

        embed = discord.Embed(
            color=0x89C4FF,
            title="pack.mcmeta Generator",
            description="生成完了!",
            timestamp=datetime.now()
        )
        embed.add_field(name="説明", value=create_codeblock(description))
        embed.add_field(name="パックバージョン", value=create_codeblock(f"({version}) {ver.rp}"))

        data: str = PackMcmeta(pack=PackMcmetaV(pack_format=ver.rp, description=description)).model_dump_json(indent=4)
        file = discord.File(io.StringIO(data), filename="pack.mcmeta")

        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)


async def setup(bot: commands.Bot):
    bot.tree.add_command(CPackMcMeta(bot))
