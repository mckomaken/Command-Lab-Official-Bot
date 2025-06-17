from datetime import datetime
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from markdownify import markdownify as md

from schemas.patch_note import PatchNote
from schemas.version_manifest import VersionManifest

JAVA_PATCH_NOTES = "https://launchercontent.mojang.com/javaPatchNotes.json/"
JAVA_VERSION_MANIFESTS = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)
SPLIT_LINE = "--------------------------"


class CNews(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cnews", description="更新情報の詳細を表示します")
    @app_commands.guild_only()
    async def cnews(self, interaction: discord.Interaction, version: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession(JAVA_PATCH_NOTES) as client:
                async with client.get("") as resp:
                    data = PatchNote.model_validate(await resp.json(content_type=None, encoding="utf-8-sig"))
                    print(data)
                    for entry in data["entries"][0]:
                        print(entry)
                        if entry["version"] == version:
                            embed = discord.Embed(
                                title=entry["image"]["title"],
                                description=md(entry["body"][:4000]) + ("..." if len(entry["body"]) > 4000 else ""),
                            )
                            embed.set_thumbnail(
                                url="https://launchercontent.mojang.com/{}".format(entry["image"]["title"])
                            )
                            await interaction.followup.send(embed=embed)
                            return
            await interaction.followup.send("バージョンが見つかりませんでした")
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました\n{e}")

    @app_commands.command(name="creference", description="更新情報を表示します")
    @app_commands.guild_only()
    async def changelog(
        self, interaction: discord.Interaction, version: Optional[str] = ""
    ):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(JAVA_VERSION_MANIFESTS) as resp:
                    data = VersionManifest.model_validate(await resp.json())

                    clsv = data.latest.snapshot
                    clrv = version or data.latest.release
                    cclrv = clrv.replace(".", "-")
                    cclsv = "" if "pre" in clsv else "snapshot-" + clsv.replace(".", "-").replace("-pre", "-pre-release-")

                    clsv2 = f"{clsv} & {clrv}" if version == "" else clrv
                    latest_embed = discord.Embed(
                        title=f"【 {clsv2} 】のchangelog",
                        color=discord.Color.orange(),
                        timestamp=datetime.now(),
                    )
                    if version == "":
                        latest_embed.add_field(
                            name=f"{SPLIT_LINE}\nLatest Snapshot Version\n{SPLIT_LINE}",
                            value="",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【English References】",
                            value=f"https://www.minecraft.net/en-us/article/minecraft-{cclsv}",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【English Wiki】",
                            value=f"https://minecraft.wiki/w/Java_Edition_{clsv}",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【Japanese Wiki】",
                            value=f"https://ja.minecraft.wiki/w/Java_Edition_{clsv}",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name=f"{SPLIT_LINE}\nLatest Release Version\n{SPLIT_LINE}",
                            value="",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【English References】",
                            value="https://www.minecraft.net/en-us/article/minecraft-java-edition-{cclrv}",
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【English Wiki】",
                            value="https://minecraft.wiki/w/Java_Edition_{}".format(
                                clrv
                            ),
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【Japanese Wiki】",
                            value="https://ja.minecraft.wiki/w/Java_Edition_{}".format(
                                clrv
                            ),
                            inline=False,
                        )
                    else:
                        if clrv.count(".") >= 1:
                            latest_embed.add_field(
                                name="【English References】",
                                value="https://www.minecraft.net/en-us/article/minecraft-java-edition-" + cclrv,
                                inline=False,
                            )
                        else:
                            latest_embed.add_field(
                                name="【English References】",
                                value="https://www.minecraft.net/en-us/article/minecraft-snapshot-" + cclrv,
                                inline=False,
                            )
                        latest_embed.add_field(
                            name="【English Wiki】",
                            value="https://minecraft.wiki/w/Java_Edition_" + clrv,
                            inline=False,
                        )
                        latest_embed.add_field(
                            name="【Japanese Wiki】",
                            value="https://ja.minecraft.wiki/w/Java_Edition_" + clrv,
                            inline=False,
                        )

                    await interaction.followup.send(embed=latest_embed)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました\n{e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CNews(bot))
