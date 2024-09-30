import io
import random
import struct
import zlib

import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock, create_embed


def create_image(width: int, height: int, color_code: str) -> io.BytesIO:
    if not (isinstance(width, int) and width > 0 and isinstance(height, int) and height > 0):
        raise ValueError("Width and Height must be positive integers")
    if not color_code.startswith('#') or len(color_code) not in (7, 9):
        raise ValueError("Color code must be in the format #RRGGBB or #RRGGBBAA")

    # Parse the color code
    r = int(color_code[1:3], 16)
    g = int(color_code[3:5], 16)
    b = int(color_code[5:7], 16)
    a = int(color_code[7:9], 16) if len(color_code) == 9 else 255

    # PNG file signature
    png_signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # Width, Height, Bit depth, Color type, Compression, Filter, Interlace
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr_chunk = struct.pack(">I", len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack(">I", ihdr_crc)

    # IDAT chunk
    row = b'\x00' + struct.pack("BBBB", r, g, b, a) * width
    idat_data = b''.join([row for _ in range(height)])
    compressed_idat_data = zlib.compress(idat_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed_idat_data) & 0xffffffff
    idat_chunk = struct.pack(">I", len(compressed_idat_data)) + b'IDAT' + compressed_idat_data + struct.pack(">I", idat_crc)

    # IEND chunk
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data) & 0xffffffff
    iend_chunk = struct.pack(">I", len(iend_data)) + b'IEND' + iend_data + struct.pack(">I", iend_crc)

    png_data = png_signature + ihdr_chunk + idat_chunk + iend_chunk

    return io.BytesIO(png_data)


def randhex() -> str:
    return hex(random.randint(0x00, 0xFF))


def get_rgb_from_hex(color_code: str) -> tuple:
    r = int(color_code[1:3], 16)
    g = int(color_code[3:5], 16)
    b = int(color_code[5:7], 16)
    if len(color_code) == 9:
        a = int(color_code[7:9], 16)
        return (r, g, b, a)
    return (r, g, b)


class CColor(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="ccolor")
        self.bot = bot

    @app_commands.command(name="preview", description="カラーコードのプレビューを行います")
    async def preview(self, interaction: discord.Interaction, color: str):
        try:
            c_color = int(color.replace("#", ""), base=16)
            cc_color = get_rgb_from_hex(color)
            image = create_image(1024, 300, color)

            file = discord.File(image, filename="color.png")

            embed = discord.Embed(
                color=c_color, title="色のプレビュー", description=color.upper()
            )
            embed.set_image(url="attachment://color.png")
            embed.add_field(
                name="10進数表記", value=create_codeblock(f"{c_color}")
            )
            embed.add_field(
                name="RGB",
                value=create_codeblock(f"{cc_color[0]}, {cc_color[1]}, {cc_color[2]}"),
            )

            await interaction.response.send_message(embed=embed, file=file)
        except ValueError:
            await interaction.response.send_message(
                embed=create_embed("エラー", "値が無効です"), ephemeral=True
            )

    @app_commands.command(name="random", description="カラーコードをランダムに出力し行います")
    async def random(self, interaction: discord.Interaction):
        try:
            color = "#" + randhex()[2:].zfill(2) + randhex()[2:].zfill(2) + randhex()[2:].zfill(2)
            c_color = int(color.replace("#", ""), base=16)
            cc_color = get_rgb_from_hex(color)  # 手動でRGBを取得
            image = create_image(1024, 300, color)

            file = discord.File(image, filename="color.png")

            embed = discord.Embed(
                color=c_color, title="色のプレビュー", description=color.upper()
            )
            embed.set_image(url="attachment://color.png")
            embed.add_field(
                name="10進数表記", value=create_codeblock(f"{c_color}")
            )
            embed.add_field(
                name="RGB",
                value=create_codeblock(f"{cc_color[0]}, {cc_color[1]}, {cc_color[2]}"),
            )

            await interaction.response.send_message(embed=embed, file=file)
        except ValueError:
            await interaction.response.send_message(
                embed=create_embed("エラー", "値が無効です"), ephemeral=True
            )


async def setup(bot: commands.Bot):
    bot.tree.add_command(CColor(bot))
