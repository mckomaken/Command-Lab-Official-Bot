import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

from config.config import config


class CBnoticetime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.notice_channel = await self.bot.fetch_channel(config.bump.channel_id)

    @app_commands.command(name="cbnoticetime", description="【運営】再起動後の通知時間設定用")
    @app_commands.describe(addminutes="入力分後に通知されます")
    @app_commands.checks.has_role(config.administrater_role_id)
    async def cbnoticetime(self, interaction: discord.Interaction, addminutes: int = 0):
        assert isinstance(self.notice_channel, discord.abc.Messageable)

        current_time = datetime.now()
        scheduled_time = current_time + timedelta(minutes=addminutes)
        formatted_scheduled_time = scheduled_time.strftime(" %Y/%m/%d %H:%M ")
        bump_image_attachment = discord.File(os.path.join(os.getenv("BASE_DIR", "."), "assets/bump.png"), filename="bump.png")

        bump_embed = discord.Embed(
            title="BUMPの時間だよ(^O^)/",
            description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
            color=0x00FFFF,
            timestamp=scheduled_time,
        )
        bump_embed.add_field(
            name="It's BUMP time (^O^)/",
            value="It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump.",
        )
        bump_embed.set_image(url="attachment://bump.png")

        await interaction.response.send_message(f"{addminutes}分後({formatted_scheduled_time}頃)に通知されます")
        await asyncio.sleep(addminutes * 60)
        await self.notice_channel.send(embed=bump_embed, file=bump_image_attachment)


async def setup(bot: commands.Bot):
    await bot.add_cog(CBnoticetime(bot))
