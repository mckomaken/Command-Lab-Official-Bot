import discord

from discord import app_commands
from discord.ext import commands
from datetime import datetime

from config import config


class CAdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cmisc", description="【運営】運営専用雑コマンド")
    @app_commands.describe(choice="選択肢")
    @app_commands.choices(choice=[
            app_commands.Choice(name="高校おめ", value="cl1"),
            app_commands.Choice(name="大学おめ", value="cl2")
    ])
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cmisc(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        if choice.value == "cl1":
            await interaction.response.send_message(embed=discord.Embed(
                title="高校合格おめでとうございます!!", color=0x2b9788
            ))
        elif choice.value == "cl2":
            await interaction.response.send_message(embed=discord.Embed(
                title="大学合格おめでとうございます!!", color=0x2b9788
            ))

    @app_commands.command(
        name="cmaintenance", description="【運営】各種お知らせ用"
    )
    @app_commands.describe(
        title="タイトル",
        description="説明",
        sub_title="サブタイトル",
        sub_description="サブ説明"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def cmaintenance(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        sub_title: str = "",
        sub_description: str = ""
    ):
        mntJST_time = datetime.now()

        mennte_embed = discord.Embed(
            title=title,
            description=description,
            color=0xff580f,
            timestamp=mntJST_time
        )
        if sub_title != "" and sub_description != "":
            mennte_embed.add_field(
                name=sub_title,
                value=sub_description,
            )

        await interaction.response.send_message(embed=mennte_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CAdminCog(bot))
