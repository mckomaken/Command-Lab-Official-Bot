import io
import random

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageColor, ImageDraw

from utils.util import create_codeblock, create_embed


class CColor(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="ccolor")
        self.bot = bot

    @app_commands.command(
        name="preview", description="カラーコードのプレビューを行います"
    )
    async def preview(self, interaction: discord.Interaction, color: str):
        try:
            c_color = int(color.replace("#", ""), base=16)
            cc_color = ImageColor.getrgb(color)
            image = Image.new("RGB", (1024, 300), color=cc_color)
            d = ImageDraw.Draw(image)
            d.rectangle((0, 0, 1024, 300), fill=cc_color)

            data = io.BytesIO()
            image.save(data, format="PNG")
            file = discord.File(io.BytesIO(data.getvalue()), filename="color.png")

            embed = discord.Embed(color=c_color, title="色のプレビュー", description=color.upper())
            embed.set_image(url="attachment://color.png")
            embed.add_field(name="10進数表記", value=create_codeblock(f"{int(str(c_color), base=10)}"))
            embed.add_field(name="RGB", value=create_codeblock(f"{cc_color[0]}, {cc_color[1]}, {cc_color[2]}"))

            await interaction.response.send_message(embed=embed, file=file)
        except ValueError:
            await interaction.response.send_message(embed=create_embed(
                "エラー", "値が無効です"
            ), ephemeral=True)

    @app_commands.command(
        name="random", description="カラーコードをランダムに出力し行います"
    )
    async def random(self, interaction: discord.Interaction):
        try:
            color = "#" + hex(random.randint(0x00, 0xFF))[2:] + hex(random.randint(0x00, 0xFF))[2:] + hex(random.randint(0x00, 0xFF))[2:]
            c_color = int(color.replace("#", ""), base=16)
            cc_color = ImageColor.getrgb(color)
            image = Image.new("RGB", (1024, 300), color=cc_color)
            d = ImageDraw.Draw(image)
            d.rectangle((0, 0, 1024, 300), fill=cc_color)

            data = io.BytesIO()
            image.save(data, format="PNG")
            file = discord.File(io.BytesIO(data.getvalue()), filename="color.png")

            embed = discord.Embed(color=c_color, title="色のプレビュー", description=color.upper())
            embed.set_image(url="attachment://color.png")
            embed.add_field(name="10進数表記", value=create_codeblock(f"{int(str(c_color), base=10)}"))
            embed.add_field(name="RGB", value=create_codeblock(f"{cc_color[0]}, {cc_color[1]}, {cc_color[2]}"))

            await interaction.response.send_message(embed=embed, file=file)
        except ValueError:
            await interaction.response.send_message(embed=create_embed(
                "エラー", "値が無効です"
            ), ephemeral=True)


async def setup(bot: commands.Bot):
    bot.tree.add_command(CColor(bot))
