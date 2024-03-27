import discord
from discord import app_commands
from discord.ext import commands

from utils.util import create_codeblock, create_embed


class ConvertView(discord.ui.View):
    def __init__(self, text: str):
        super().__init__(timeout=None)
        self.text = text

    @discord.ui.button(label="titleに変換", style=discord.ButtonStyle.green)
    async def convert_title(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.send_message(
            embed=create_embed(title="コマンド", description=create_codeblock(
                "/title @a title {\"text\":\"" + self.text + "\"}"
            ))
        )

    @discord.ui.button(label="tellrawに変換", style=discord.ButtonStyle.green)
    async def convert_tellraw(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.send_message(
            embed=create_embed(title="コマンド", description=create_codeblock(
                "/tellraw @a {\"text\":\"" + self.text + "\"}"
            ))
        )


@app_commands.guild_only()
class CUnicode(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            name="cunicode",
            description="UNICODEエスケープシーケンスのエンコード/デコードをします。"
        )
        self.bot = bot

    @app_commands.command(name="encode", description="UNICODEエスケープシーケンスのエンコードをします。")
    @app_commands.describe(text="エンコードする文字列")
    @app_commands.guild_only()
    async def unicode_encode(self, interaction: discord.Interaction, text: str):
        data = text.encode("unicode-escape").decode()

        embed = discord.Embed(
            title="Unicodeエスケープシーケンス変換 - エンコード",
            description=create_codeblock(data)
        )

        await interaction.response.send_message(embed=embed, view=ConvertView(data))

    @app_commands.command(name="decode", description="UNICODEエスケープシーケンスのデコードをします。")
    @app_commands.describe(text="デコードする文字列")
    @app_commands.guild_only()
    async def unicode_decode(self, interaction: discord.Interaction, text: str):
        data = text.encode().decode("unicode-escape")

        embed = discord.Embed(
            title="Unicodeエスケープシーケンス変換 - デコード",
            description=create_codeblock(data)
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    bot.tree.add_command(CUnicode(bot))
