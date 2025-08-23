import asyncio
import logging
import logging.config
import os
from datetime import datetime
from os import listdir, path

import aiofiles
import discord
import yaml
from discord import app_commands
from discord.abc import User
from discord.ext import commands

from config.config import config
from utils.setup import setup, setup_mcdata

logger = logging.getLogger("root")

# ステータス定義 ({key}を{value}中)
STATUSES = [
    ("JavaEdition", "playing", 120),
    ("BedrockEdition", "playing", 120),
    ("BugEdition", "playing", 10),
    ("マイクラのコマンドを勉強中", "playing", 100),
    ("discord.pyとpythonを勉強中", "playing", 100),
    ("Javaを勉強中", "playing", 100),
    ("JavaScriptを勉強中", "playing", 100),
    ("コマ研Botはいつでもあなたのメッセージを見ている", "watching", 20),
    ("大体何でもできるのだ♪", "watching", 30),
    ("私はボットです", "playing", 30),
    ("Netflixで映画", "watching", 30),
    ("ポテトをツンツン中", "playing", 30),
    ("YouTube", "watching", 100),
    ("春菊を調理中", "playing", 120),
    ("春菊の配信", "watching", 10),
    ("YouTube", "watching", 100),
    ("Spotify", "listening", 100),
]


class CommandLabBot(commands.Bot):
    status_index: int

    def __init__(self) -> None:
        super().__init__(
            command_prefix=config.prefix,
            intents=discord.Intents.all(),
            owner_ids=config.owner_ids,
        )
        self.status_index = 0

    async def is_owner(self, user: User) -> bool:
        return user.id in config.owner_ids

    async def change_status(self):
        await self.wait_until_ready()
        name, activity_type, interval = STATUSES[self.status_index]
        if activity_type == "playing":  # ~をプレイ中
            activity = discord.Activity(type=discord.ActivityType.playing, name=name)
        elif activity_type == "streaming":  # ~を配信中
            activity = discord.Streaming(name=name, url="your_stream_url")
        elif activity_type == "listening":  # ~を再生中
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
        elif activity_type == "watching":  # ~を視聴中
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        elif activity_type == "competing":  # ~に参戦中
            activity = discord.Activity(type=discord.ActivityType.competing, name=name)
        else:  # その他
            activity = discord.Activity(type=discord.ActivityType.custom, name=name)

        await self.change_presence(activity=activity)
        self.status_index += 1
        if self.status_index >= len(STATUSES):
            self.status_index = 0
        await asyncio.sleep(interval)
        asyncio.create_task(self.change_status())

    async def setup_hook(self) -> None:
        if "*" in config.enabled_features:
            for name in listdir("cogs"):
                if name != "__pycache__" and not name.startswith("_"):
                    modname = name.replace(".py", "")
                    f = f"cogs.{modname}"
                    await self.load_extension(f)
                    logger.info(f"機能 [{f}] が正常にロードされました。")
        else:
            for f in config.enabled_features:
                await self.load_extension(f)
                logger.info(f"機能 [{f}] が正常にロードされました。")
        await self.tree.sync()

        self.loop.create_task(self.change_status())

    @classmethod
    async def start(cls, token: str) -> None:
        logging.config.dictConfig(
            yaml.load(
                await (await aiofiles.open(
                    path.join(os.getenv("BASE_DIR", "."), "data/logging.yaml")
                )).read(),
                Loader=yaml.SafeLoader,
            )
        )
        await setup()
        await setup_mcdata()
        client = cls()

        async with client:

            @client.event
            async def on_ready():
                start_embed = discord.Embed(
                    title="BOTが起動しました！",
                    description="BOT has been started!",
                    color=0xFFD700,
                    timestamp=datetime.now(),
                )

                logger.info("BOTが起動しました")
                if config.start_notice_channel is not None:
                    start_notice_channel = await client.fetch_channel(
                        config.start_notice_channel
                    )
                    await start_notice_channel.send(embed=start_embed)

            @client.event
            async def on_message(message: discord.Message):
                if not message.author.bot:
                    if message.author.id in client.owner_ids or []:
                        await client.process_commands(message)

                if client.user in message.mentions and message.reference is None:
                    if message.author.bot:
                        return
                    await message.channel.send(
                        f"{message.author.mention}呼んだ？わからないことがあったら以下のコマンドを実行してみてね(^^♪\n> 全コマンド雑説明: </chelp-all:1383117112628871198>\n> コマンド別説明　: </chelp:1218483030247604265>", silent=True
                    )

            @client.tree.error
            async def on_error(
                ctx: discord.Interaction, error: app_commands.AppCommandError
            ):
                if isinstance(error, app_commands.MissingRole) or isinstance(
                    error, app_commands.MissingPermissions
                ):
                    await ctx.response.send_message("権限あらへんで(関西弁)", ephemeral=True)
                else:
                    logger.error(error)

            return await super().start(client, token=token)

    async def close(self) -> None:
        logger.info("機能のアンロードを行っています...")
        for e in list(self.extensions.keys()):
            await self.unload_extension(e)
        logger.info("機能のアンロードが完了しました。プロセスを終了します")
        return await super().close()


if config.token == "FILE":
    config.token = open("..\\CMTK.txt", mode="r").read()
if config.token == "ENV":
    config.token = os.getenv("TOKEN")

if __name__ == "__main__":
    asyncio.run(CommandLabBot.start(token=config.token))
