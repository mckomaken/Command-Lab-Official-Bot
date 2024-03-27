import os
from datetime import datetime, timedelta
from typing import Optional

import discord
from discord.ext import commands, tasks
from pydantic import BaseModel

from config.config import config

JA_BUMP_MESSAGE = """
BUMPの時間になったよ♪
</bump:947088344167366698> って打ってね

なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。
"""

EN_BUMP_MESSAGE = """It's BUMP time♪
Please send </bump:947088344167366698>

If you bumped within 30 minutes on another server, you may not be able to bump.
"""


class BumpData(BaseModel):
    last_timestamp: Optional[float] = None
    notified: Optional[bool] = None


class BumpNofiticationCog(commands.Cog):
    bump_data: BumpData

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.bump_data = BumpData()

    @tasks.loop(seconds=1)
    async def bump_check_task(self):
        if self.bump_data.last_timestamp is None:
            return
        last = datetime.fromtimestamp(self.bump_data.last_timestamp) + timedelta(hours=2)
        now = datetime.now()

        if last < now and not self.bump_data.notified:
            bump_file = discord.File("./assets/bump.png", filename="bump.png")

            bump_embed = discord.Embed(
                title="BUMPの時間だよ(^O^)／",
                description=JA_BUMP_MESSAGE,
                color=0x00ffff,
                timestamp=now
            )
            bump_embed.add_field(
                name="It's BUMP time (^O^)/",
                value=EN_BUMP_MESSAGE
            )
            bump_embed.set_image(url="attachment://bump.png")

            channel = await self.bot.fetch_channel(config.bump.channel_id)
            await channel.send(embed=bump_embed, file=bump_file)

            self.bump_data.notified = True

    async def cog_load(self):
        if not os.path.exists("./tmp/bump_data.json"):
            open("./tmp/bump_data.json", mode="w").write(BumpData().model_dump_json())

        self.bump_data = BumpData.model_validate_json(
            open("./tmp/bump_data.json", mode="rb").read()
        )

        self.bump_check_task.start()

    async def cog_unload(self):
        self.bump_check_task.cancel()
        open("./tmp/bump_data.json", mode="w").write(self.bump_data.model_dump_json())


async def setup(bot: commands.Bot):
    await bot.add_cog(BumpNofiticationCog(bot))
