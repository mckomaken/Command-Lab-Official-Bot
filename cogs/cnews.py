from datetime import datetime
from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from markdownify import markdownify as md

from schemas.patch_note import PatchNote
from schemas.version_manifest import VersionManifest


class CNews(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cnews", description="更新情報の詳細を表示します")
    @app_commands.guild_only()
    async def cnews(self, interaction: discord.Interaction, version: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get("https://launchercontent.mojang.com/javaPatchNotes.json") as resp:
                    data = PatchNote.model_validate(await resp.json())
                    for entry in data.entries:
                        if entry.version == version:
                            embed = discord.Embed(
                                title=entry.title,
                                description=md(entry.body[:4000]) + ("..." if len(entry.body) > 4000 else "")
                            )
                            embed.set_thumbnail(url="https://launchercontent.mojang.com" + entry.image.url)
                            await interaction.followup.send(embed=embed)
                            return
            await interaction.followup.send("バージョンが見つかりませんでした")
        except Exception:
            await interaction.followup.send("エラーが発生しました")

    @app_commands.command(name="creference", description="更新情報を表示します")
    @app_commands.guild_only()
    async def changelog(self, interaction: discord.Interaction, version: Optional[str] = ""):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json") as resp:
                    data = VersionManifest.model_validate(await resp.json())

                    clsv: str = data.latest.snapshot
                    clrv: str = version or data.latest.release
                    cclrv: str = clrv.replace(".", "-")

                    clsv2 = f"{clsv} & {clrv}" if version == "" else clrv
                    latest_embed = discord.Embed(
                        title=f"【 {clsv2} 】のchangelog",
                        color=discord.Color.orange(),
                        timestamp=datetime.now()
                    )
                    if version == "":
                        latest_embed.add_field(
                            name="--------------------------\nLatest Snapshot Version\n--------------------------", value="", inline=False
                        )
                        latest_embed.add_field(
                            name="【English References】", value="https://www.minecraft.net/en-us/article/minecraft-snapshot-" + clsv, inline=False
                        )
                        latest_embed.add_field(name="【English Wiki】", value="https://minecraft.wiki/w/Java_Edition_" + clsv, inline=False)
                        latest_embed.add_field(name="【Japanese Wiki】", value="https://ja.minecraft.wiki/w/Java_Edition_" + clsv, inline=False)
                        latest_embed.add_field(
                            name="------------------------\nLatest Release Version\n------------------------", value="", inline=False
                        )
                        latest_embed.add_field(
                            name="【English References】", value="https://www.minecraft.net/en-us/article/minecraft-java-edition-" + cclrv, inline=False
                        )
                        latest_embed.add_field(name="【English Wiki】", value="https://minecraft.wiki/w/Java_Edition_" + clrv, inline=False)
                        latest_embed.add_field(name="【Japanese Wiki】", value="https://ja.minecraft.wiki/w/Java_Edition_" + clrv, inline=False)
                    else:
                        if clrv.count(".") >= 1:
                            latest_embed.add_field(
                                name="【English References】",
                                value="https://www.minecraft.net/en-us/article/minecraft-java-edition-" + cclrv,
                                inline=False
                            )
                        else:
                            latest_embed.add_field(
                                name="【English References】",
                                value="https://www.minecraft.net/en-us/article/minecraft-snapshot-" + cclrv,
                                inline=False
                            )
                        latest_embed.add_field(name="【English Wiki】", value="https://minecraft.wiki/w/Java_Edition_" + clrv, inline=False)
                        latest_embed.add_field(name="【Japanese Wiki】", value="https://ja.minecraft.wiki/w/Java_Edition_" + clrv, inline=False)

                    await interaction.followup.send(embed=latest_embed)
        except Exception:
            await interaction.followup.send("エラーが発生しました")


async def setup(bot: commands.Bot):
    await bot.add_cog(CNews(bot))
