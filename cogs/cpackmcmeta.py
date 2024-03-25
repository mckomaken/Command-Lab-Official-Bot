import discord

from discord.ext import commands
from discord import app_commands

from config import pack_versions
from table2ascii import table2ascii, Alignment, PresetStyle

VERSION_NOT_FOUND = discord.Embed(
    title="エラー", description="バージョンが見つかりません。", color=0xff0000
)


def escape(data: str):
    return f"```\n{data}```"


@app_commands.guild_only()
class CPackMcMeta(commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="cpackmcmeta")
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
            description=escape(
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
            description=escape(
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
        interaction: discord.Interaction, version: str = ""
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


async def setup(bot: commands.Bot):
    bot.add_cog(CPackMcMeta(bot))
