import discord

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from discord.ext import commands, tasks

from config import config


class BumpData(BaseModel):
    last_timestamp: Optional[float] = None
    notified: Optional[bool] = None


class BumpNofiticationCog(commands.Cog):
    bump_data: BumpData

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @tasks.loop(seconds=1)
    async def bump_check_task(self):
        last = datetime.fromtimestamp(self.bump_data.last_timestamp) + timedelta(hours=2)
        now = datetime.now()

        if last < now and not self.bump_data.notified:
            bump_file = discord.File("bump.png", filename="bump.png")

            bump_embed = discord.Embed(
                title="BUMPの時間だよ(^O^)／",
                description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
                color=0x00ffff,
                timestamp=now
            )
            bump_embed.add_field(
                name="It's BUMP time (^O^)/",
                value="It's BUMP time♪ \n Please send </bump:947088344167366698>\n\n If you bumped within 30 minutes on another server, you may not be able to bump."
            )
            bump_embed.set_image(url="attachment://bump.png")

            channel = await self.bot.fetch_channel(config.bump.channel_id)
            await channel.send(embed=bump_embed, file=bump_file)

            self.bump_data.notified = True

    async def cog_load(self):
        self.bump_check_task.start()

    async def cog_unload(self):
        self.bump_check_task.cancel()
        open("./tmp/bump_data.json", mode="w").write(self.bump_data.model_dump_json())
