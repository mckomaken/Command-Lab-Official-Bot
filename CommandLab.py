import asyncio
import logging
import logging.config
from datetime import datetime
from os import listdir, path
import os

import aiofiles
import discord
import yaml
from discord import app_commands
from discord.abc import User
from discord.ext import commands

from config.config import config
from utils.setup import setup, setup_mcdata

logger = logging.getLogger("root")


class CommandLabBot(commands.Bot):
    status_index: int

    def __init__(self) -> None:
        super().__init__(
            command_prefix=config.prefix,
            intents=discord.Intents.all(),
            owner_ids=config.users.owner_ids,
        )
        self.status_index = 0

    async def is_owner(self, user: User) -> bool:
        return user.id in config.users.owner_ids

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
                if config.channels.komaken_bot_development_room is not None:
                    start_notice_channel = await client.fetch_channel(
                        config.channels.komaken_bot_development_room
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
                    await message.reply(
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
