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
        last = datetime.fromtimestamp(self.bump_data.last_timestamp) + timedelta(
            hours=2
        )
        now = datetime.now()

        if last < now and not self.bump_data.notified:
            bump_file = discord.File(os.path.join(os.getenv("BASE_DIR", "."), "assets/bump.png"), filename="bump.png")

            bump_embed = discord.Embed(
                title="BUMPの時間だよ(^O^)／",
                description=JA_BUMP_MESSAGE,
                color=0x00FFFF,
                timestamp=now,
            )
            bump_embed.add_field(name="It's BUMP time (^O^)/", value=EN_BUMP_MESSAGE)
            bump_embed.set_image(url="attachment://bump.png")

            channel = await self.bot.fetch_channel(config.bump.channel_id)
            await channel.send(embed=bump_embed, file=bump_file)

            self.bump_data.notified = True

    async def cog_load(self):
        if not os.path.exists(os.path.join(os.getenv("TMP_DIRECTORY", "./.tmp"), "bump_data.png")):
            open(os.path.join(os.getenv("TMP_DIRECTORY", "./.tmp"), "bump_data.png"), mode="w").write(BumpData().model_dump_json())

        self.bump_data = BumpData.model_validate_json(
            open(os.path.join(os.getenv("TMP_DIRECTORY", "./.tmp"), "bump_data.png"), mode="rb").read()
        )

        self.bump_check_task.start()

    async def cog_unload(self):
        self.bump_check_task.cancel()
        open(os.path.join(os.getenv("TMP_DIRECTORY", "./.tmp"), "bump_data.png"), mode="w").write(self.bump_data.model_dump_json())

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.channel.id == config.bump.channel_id:
            if message.content.startswith("!d bump"):
                await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")

            elif message.content.startswith("/bump"):
                await message.channel.send(
                    embed=discord.Embed(
                        title="BUMPを実行出来てないよ!!",
                        color=0x00BFFF,
                        timestamp=datetime.now(),
                    )
                )

        if message.author.id == config.bump.disboard_id:
            embeds = message.embeds

            if embeds is not None and len(embeds) != 0:
                if "表示順をアップしたよ" in (embeds[0].description or ""):
                    JST_time = datetime.now()
                    master = JST_time + timedelta(hours=2)
                    fmaster = master.strftime(" %Y/%m/%d %H:%M:%S ")
                    notice_channel = await self.bot.fetch_channel(
                        config.bump.channel_id
                    )

                    bump_notice_embed = discord.Embed(
                        title="BUMPを検知しました",
                        description=f"次は {fmaster} 頃に通知するね～ \n ",
                        color=0x00BFFF,
                        timestamp=JST_time,
                    )
                    bump_notice_embed.add_field(
                        name="BUMP detected",
                        value=f"The next time you can BUMP is {fmaster}",
                    )

                    another_channel_bump_notice_embed = discord.Embed(
                        title="別のチャンネルでBUMPを検知しました",
                        description=f"次はここのチャンネルで {fmaster} 頃に通知するね～ \n ",
                        color=0x00BFFF,
                        timestamp=JST_time,
                    )
                    another_channel_bump_notice_embed.add_field(
                        name="BUMP detected on another channel",
                        value=f"The next time you can BUMP is {fmaster} in this channel",
                    )

                    caution_another_channel_bump_notice_embed = discord.Embed(
                        title="ここのチャンネルでBUMPしないでね",
                        description=f"次からは {notice_channel.mention} でBUMPしてね \n ",
                        color=0xFF4500,
                        timestamp=JST_time,
                    )
                    caution_another_channel_bump_notice_embed.add_field(
                        name="Don't BUMP on this channel here",
                        value=f"Next time, BUMP at {notice_channel.mention}!",
                    )

                    if message.channel.id != config.bump.channel_id:
                        await notice_channel.send(
                            "＼(^o^)／", embed=another_channel_bump_notice_embed
                        )
                        await message.channel.send(
                            embed=caution_another_channel_bump_notice_embed
                        )
                    else:
                        await message.channel.send(embed=bump_notice_embed)

                    self.bump_data.last_timestamp = datetime.now().timestamp()
                    self.bump_data.notified = False


async def setup(bot: commands.Bot):
    await bot.add_cog(BumpNofiticationCog(bot))
