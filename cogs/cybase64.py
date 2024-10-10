import base64

import discord
from discord import app_commands
from discord.ext import commands

from config.config import config
from utils.util import create_codeblock, create_embed


class UrlView(discord.ui.View):
    def __init__(self, text: str):
        super().__init__(timeout=None)
        self.text = text

    @discord.ui.button(label="送信内容を見る", style=discord.ButtonStyle.red)
    async def convert_title(
        self, interaction: discord.Interaction, item: discord.ui.Item
    ):
        await interaction.response.send_message(
            embed=create_embed(title="送信内容", description=(f"{self.text}")),
            ephemeral=True,
        )


class CYbase64(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cybase64", description="y談用のBase64変換です")
    @app_commands.describe(text="送信したい内容を書いてください")
    async def cybase64(self, interaction: discord.Interaction, text: str):
        send_channel = await self.bot.fetch_channel(config.y_channel.channel_id)
        admin_channel = await self.bot.fetch_channel(config.y_channel.admin_channel_id)
        yembed = discord.Embed(
            color=0xD51EBE,
            title=interaction.user.display_name,
            description=create_codeblock(base64.b64encode(text.encode()).decode()),
        )
        admin_embed = discord.Embed(
            color=0xD51EBE,
            title=interaction.user.display_name,
            description=f"y談送信内容\n{text}",
        )
        if interaction.channel == send_channel:
            await interaction.response.send_message("送信しました", ephemeral=True)
            await send_channel.send(embed=yembed, view=UrlView(text))
            await admin_channel.send(embed=admin_embed)
        else:
            await interaction.response.send_message(
                "チャンネル違うよ！", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(CYbase64(bot))
