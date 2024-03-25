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


RP_ALL_VERSIONS = [
    "13w24a-1.8.9",
    "15w31a-1.10.2",
    "16w32a-18w47a",
    "18w48a-19w46b",
    "1.15-pre1-1.16.2-pre3",
    "1.16.2-rc1-1.16.5",
    "20w45a-21w38a",
    "21w39a-1.18.2",
    "22w11a-1.19.2",
    "---",
    "22w42a-22w44a",
    "22w45a-23w07a",
    "1.19.4-pre1-23w13a",
    "23w14a-23w16a",
    "23w17a-1.20.1",
    "23w31a",
    "23w32a-1.20.2-pre1",
    "1.20.2-pre2-23w41a",
    "23w42a",
    "23w43a-23w44a",
    "23w45a-23w46a",
    "1.20.3-pre1-23w51b",
    "---",
    "24w03a-24w04a",
    "24w05a-24w05b",
    "24w06a-24w07a",
    "---",
    "24w09a-24w10a",
    "24w11a",
    "24w12a"
]

DP_ALL_VERSIONS = [
    "17w48a-19w46b",
    "1.15-pre1-1.16.2-pre3",
    "1.16.2-rc1-1.16.5",
    "20w46a-1.17.1",
    "21w37a-22w07a",
    "1.18.2-pre1-1.18.2",
    "22w11a-1.19.3",
    "23w03a-23w05a",
    "23w06a-1.19.4",
    "23w12a-23w14a",
    "23w16a-23w17a",
    "23w18a-1.20.1",
    "23w31a",
    "23w32a-23w35a",
    "1.20.2-pre1-1.20.2",
    "23w40a",
    "23w41a",
    "23w42a",
    "23w43a-23w43b",
    "23w44a",
    "23w45a",
    "23w46a",
    "1.20.3-pre1-1.20.4",
    "23w51a-23w51b",
    "24w03a",
    "24w04a",
    "24w05a-24w05b",
    "24w06a",
    "24w07a",
    "24w09a",
    "24w10a",
    "24w11a",
    "24w12a"
]


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

        body = []
        i = 0
        for k, v in pack_versions.versions.items():
            if v.dp != -1:
                body.append((v.dp, DP_ALL_VERSIONS[i], k))
                i += 1

        embed = discord.Embed(
            title="データパックバージョン一覧",
            description=create_codeblock(
                table2ascii(
                    header=["Format Version", "All Version", "Release Version"],
                    body=body,
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

        body = []
        i = 0
        for k, v in pack_versions.versions.items():
            if v.rp != -1:
                body.append((v.rp, RP_ALL_VERSIONS[i], k))
                i += 1

        embed = discord.Embed(
            title="リソースパックバージョン一覧",
            description=create_codeblock(
                table2ascii(
                    header=["Format Version", "All Version", "Release Version"],
                    body=body,
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
