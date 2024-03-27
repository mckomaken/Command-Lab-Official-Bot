
import discord
from discord import app_commands
from discord.ext import commands

from config.config import config


class CDebugCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="creload", description="reload")
    @app_commands.guild_only()
    @app_commands.checks.has_role(config.administrater_role_id)
    async def creload(self, interaction: discord.Interaction):
        for e in list(self.bot.extensions.keys()):
            await self.bot.reload_extension(e)

        await interaction.response.send_message("Successfully reloaded all cogs")


async def setup(bot: commands.Bot):
    await bot.add_cog(CDebugCog(bot))
