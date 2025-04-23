from discord.ext import commands
# from datetime import datetime, timedelta
from discord import app_commands, Interaction
import discord
# from config.config import config
# from typing import Optional
import random


async def coregacha(interaction: Interaction):
    num = random.randint(1, 100000)
    if num >= 99999:
        og1_embed = discord.Embed(
            title="ガチャ結果",
            description="# ネザライト",
            color=0xff9b37
        )
        og1_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og1_embed.add_field(name="【ネザライト】", value=f"No.{num:06} / (確率:0.00002%)")
        og1_embed.set_footer(text="ネザライト>>>ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file1 = discord.File("assets/ore_gacha/Netherite_Ingot.png", filename="Netherite_Ingot.png")
        og1_embed.set_thumbnail(url="attachment://Netherite_Ingot.png")
        await interaction.response.send_message(embed=og1_embed, file=file1)

    elif num >= 94008:
        og2_embed = discord.Embed(
            title="ガチャ結果",
            description="# ダイヤモンド",
            color=0xff9b37
        )
        og2_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og2_embed.add_field(name="【ダイヤ】", value=f"No.{num:06} / (確率:5.992%)")
        og2_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file2 = discord.File("assets/ore_gacha/Diamond.png", filename="Diamond.png")
        og2_embed.set_thumbnail(url="attachment://Diamond.png")
        await interaction.response.send_message(embed=og2_embed, file=file2)

    elif num >= 87639:
        og3_embed = discord.Embed(
            title="ガチャ結果",
            description="# 金",
            color=0xff9b37
        )
        og3_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og3_embed.add_field(name="【金】", value=f"No.{num:06} / (確率:6.368%)")
        og3_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file3 = discord.File("assets/ore_gacha/Gold_Ingot.png", filename="Gold_Ingot.png")
        og3_embed.set_thumbnail(url="attachment://Gold_Ingot.png")
        await interaction.response.send_message(embed=og3_embed, file=file3)

    elif num >= 81661:
        og4_embed = discord.Embed(
            title="ガチャ結果",
            description="# ラピスラズリ",
            color=0xff9b37
        )
        og4_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og4_embed.add_field(name="【ラピス】", value=f"No.{num:06} / (確率:5.978%)")
        og4_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file4 = discord.File("assets/ore_gacha/Lapis_Lazuli.png", filename="Lapis_Lazuli.png")
        og4_embed.set_thumbnail(url="attachment://Lapis_Lazuli.png")
        await interaction.response.send_message(embed=og4_embed, file=file4)

    elif num >= 73007:
        og5_embed = discord.Embed(
            title="ガチャ結果",
            description="# レッドストーン",
            color=0xff9b37
        )
        og5_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og5_embed.add_field(name="【RS】", value=f"No.{num:06} / (確率:8.654%)")
        og5_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file5 = discord.File("assets/ore_gacha/Redstone_Dust.png", filename="Redstone_Dust.png")
        og5_embed.set_thumbnail(url="attachment://Redstone_Dust.png")
        await interaction.response.send_message(embed=og5_embed, file=file5)

    elif num >= 55221:
        og6_embed = discord.Embed(
            title="ガチャ結果",
            description="# 鉄",
            color=0xff9b37
        )
        og6_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og6_embed.add_field(name="【鉄】", value=f"No.{num:06} / (確率:17.786%)")
        og6_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file6 = discord.File("assets/ore_gacha/Iron_Ingot.png", filename="Iron_Ingot.png")
        og6_embed.set_thumbnail(url="attachment://Iron_Ingot.png")
        await interaction.response.send_message(embed=og6_embed, file=file6)

    elif num >= 18069:
        og6_embed = discord.Embed(
            title="ガチャ結果",
            description="# 銅",
            color=0xff9b37
        )
        og6_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og6_embed.add_field(name="【銅】", value=f"No.{num:06} / (確率:37.152%)")
        og6_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file6 = discord.File("assets/ore_gacha/Copper_Ingot.png", filename="Copper_Ingot.png")
        og6_embed.set_thumbnail(url="attachment://Copper_Ingot.png")
        await interaction.response.send_message(embed=og6_embed, file=file6)

    elif num >= 2:
        og7_embed = discord.Embed(
            title="ガチャ結果",
            description="# 石炭",
            color=0xff9b37
        )
        og7_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og7_embed.add_field(name="【石炭】", value=f"No.{num:06} / (確率:18.069%)")
        og7_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭")
        file7 = discord.File("assets/ore_gacha/Coal.png", filename="Coal.png")
        og7_embed.set_thumbnail(url="attachment://Coal.png")
        await interaction.response.send_message(embed=og7_embed, file=file7)

    else:
        og8_embed = discord.Embed(
            title="ガチャ結果",
            description="# 腐った肉",
            color=0xff9b37
        )
        og8_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og8_embed.add_field(name="【腐肉】", value=f"No.{num:06} / (確率:0.00001%)")
        og8_embed.set_footer(text="ダイヤ>金>ラピス>RS>鉄>銅>石炭>>>腐肉")
        file8 = discord.File("assets/ore_gacha/Rotten_Flesh.png", filename="Rotten_Flesh.png")
        og8_embed.set_thumbnail(url="attachment://Rotten_Flesh.png")
        await interaction.response.send_message(embed=og8_embed, file=file8)


class COregacha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="core-gacha", description="鉱石ガチャコマンド")
    async def coregachacom(self, interaction: discord.Interaction):
        # send_channel = await self.bot.fetch_channel(config.omikuzi_chid)
        # omdb = session1.query(Omikuzi).filter_by(userid=interaction.user.id).first()
        # if not omdb:
        #     session1.add(Omikuzi(userid=interaction.user.id, username=interaction.user.name, ddao=False))
        #     session1.commit()
        # if interaction.channel == send_channel:
        #     if omdb.ddao is True:
        #         await interaction.response.send_message("今日はもうおみくじ引いてるから引けないよ！", ephemeral=True)
        #     else:
        await coregacha(interaction)
        # else:
        #     await interaction.response.send_message("このチャンネルでは送信できないよ!\n<#1332649934763200584>で実行してね", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(COregacha(bot))
