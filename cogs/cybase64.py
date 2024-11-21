from discord.ext import commands
import base64
import discord
from discord import app_commands

from utils.util import create_codeblock, create_embed
from config.config import config


class UrlView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)
        self.url = url

    @discord.ui.button(label="送信内容を見る", style=discord.ButtonStyle.red, custom_id="ydan")
    async def convert_url(
        self, interaction: discord.Interaction, item: discord.ui.Item
    ):
        await interaction.response.send_message(
            embed=create_embed(
                title="送信内容",
                description=(
                    f"{self.url}"
                )
            ),
            ephemeral=True,
        )


class CYbase64(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cybase64", description="y談用のBase64変換です")
    @app_commands.describe(url="URLを書いてください(変換されます)", text="送信したい文章を書いてください(任意・変換されません)")
    async def cybase64(self, interaction: discord.Interaction, url: str, text: str = None):
        send_channel = await self.bot.fetch_channel(config.y_channel)
        admin_channel = await self.bot.fetch_channel(config.cmdbot_log)
        text = text.replace("\\n", "\n")
        yembed = discord.Embed(
            color=0xd51ebe,
            title=interaction.user.display_name,
            description=create_codeblock(base64.b64encode(url.encode()).decode()),
        )
        admin_embed = discord.Embed(
            color=0xd51ebe,
            title=interaction.user.display_name,
            description=f"y談送信内容\n{text}\n{url}"
        )
        if interaction.channel == send_channel:
            await interaction.response.send_message("送信しました", ephemeral=True)
            await send_channel.send(text, embed=yembed, view=UrlView(url))
            await admin_channel.send(embed=admin_embed)
        else:
            await interaction.response.send_message("チャンネル違うよ！", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CYbase64(bot))
    bot.add_view(UrlView(bot.tree))
