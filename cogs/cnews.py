from discord import app_commands
import discord
import aiohttp
from markdownify import markdownify as md
from discord.ext import commands
from pydantic import BaseModel


class PatchNoteImage(BaseModel):
    url: str
    title: str


class PatchNoteEntry(BaseModel):
    title: str
    type: str
    version: str
    image: PatchNoteImage
    body: str


class PatchNote(BaseModel):
    entries: list[PatchNoteEntry]
    version: int


class CNews(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cnews")
    @app_commands.guild_only()
    async def cnews(self, interaction: discord.Interaction, version: str):
        await interaction.response.defer()
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


async def setup(bot: commands.Bot):
    await bot.add_cog(CNews(bot))
