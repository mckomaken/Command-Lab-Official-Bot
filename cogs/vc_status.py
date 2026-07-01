from discord.ext import commands
from discord import app_commands
import discord

class VCStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="vcstatus", description="VCチャンネルのステータスメッセージを変更します")
    @app_commands.describe(message="ステータスメッセージ")
    async def vcstatus(
        self, interaction: discord.Interaction,
        message:str
    ):
        channel = interaction.channel
        if not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message("エラー：VCのテキストチャンネルで実行してください！", ephemeral=True)
        else:
            await channel.edit(status=message)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(VCStatus(bot))
