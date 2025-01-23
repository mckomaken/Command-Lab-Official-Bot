from discord.ext import commands
# from datetime import datetime, timedelta
from discord import app_commands, Interaction
import discord
# from config.config import config
from typing import Optional
import random


async def omikuzi1(interaction: Interaction):
    num = random.randint(1, 1000)
    if num >= 900:
        om1_1_embed = discord.Embed(
            description="おみくじ結果\n# 大吉",
            color=0xffff00
        )
        await interaction.response.send_message(embed=om1_1_embed)
    elif num >= 730:
        om1_2_embed = discord.Embed(
            description="おみくじ結果\n# 吉",
            color=0xffff00
        )
        await interaction.response.send_message(embed=om1_2_embed)
    elif num >= 380:
        om1_3_embed = discord.Embed(
            description="おみくじ結果\n# 中吉",
            color=0xffff00
        )
        await interaction.response.send_message(embed=om1_3_embed)
    elif num >= 260:
        om1_4_embed = discord.Embed(
            description="おみくじ結果\n# 小吉",
            color=0xffff00
        )
        await interaction.response.send_message(embed=om1_4_embed)
    else:
        om1_5_embed = discord.Embed(
            description="おみくじ結果\n# 末吉",
            color=0xffff00
        )
        await interaction.response.send_message(embed=om1_5_embed)


async def omikuzi2(interaction: Interaction):
    num = random.randint(1, 1000)
    if num >= 930:
        om2_1_embed = discord.Embed(
            description="おみくじ結果\n# 大吉",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_1_embed)
    elif num >= 790:
        om2_2_embed = discord.Embed(
            description="おみくじ結果\n# 吉",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_2_embed)
    elif num >= 470:
        om2_3_embed = discord.Embed(
            description="おみくじ結果\n# 中吉",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_3_embed)
    elif num >= 380:
        om2_4_embed = discord.Embed(
            description="おみくじ結果\n# 小吉",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_4_embed)
    elif num >= 150:
        om2_5_embed = discord.Embed(
            description="おみくじ結果\n# 末吉",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_5_embed)
    elif num >= 50:
        om2_6_embed = discord.Embed(
            description="おみくじ結果\n# 半凶",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_6_embed)
    else:
        om2_7_embed = discord.Embed(
            description="おみくじ結果\n# 凶",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=om2_7_embed)


class COmikuzi(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="comikuzi", description="おみくじコマンド")
    @app_commands.describe(choice="選択肢", help="【初期値(未記入) : False】True : helpが表示されます ・ False : おみくじがひけます")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name="太宰府天満宮バージョン", value="om1"),
            app_commands.Choice(name="北野天満宮バージョン", value="om2"),
            app_commands.Choice(name="オリジナルバージョン", value="om3")
        ]
    )
    async def cpresent(self, interaction: discord.Interaction, choice: Optional[str] = None, help: Optional[bool] = False):
        if help is True:  # help用のエンベッド表示
            await interaction.response.send_message("送信しました", ephemeral=True)
        else:  # おみくじ
            choosenum = random.randint(1, 3)
            if choice == "om1":
                await omikuzi1(interaction)
            elif choice == "om2":
                await omikuzi2(interaction)
            elif choice == "om3":
                await interaction.response.send_message("まだないよ(笑)", ephemeral=True)
            else:
                if choosenum == 1:
                    await omikuzi1(interaction)
                elif choosenum == 2:
                    await omikuzi2(interaction)
                else:
                    await interaction.response.send_message("まだないよ(笑)", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(COmikuzi(bot))
