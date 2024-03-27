import asyncio
import logging
import logging.config
from datetime import datetime, timedelta

import aiofiles
import discord
import yaml
from discord import app_commands
from discord.abc import User
from discord.ext import commands

from config.config import config
from utils.setup import setup, setup_mcdata

logger = logging.getLogger("root")


class CustomBot(commands.Bot):
    async def is_owner(self, user: User) -> bool:
        return user.id in config.owner_ids


client = CustomBot(
    intents=discord.Intents.all(),
    command_prefix=config.prefix,
    owner_ids=config.owner_ids
)


status = discord.Activity(
    type=discord.ActivityType.playing,
    name=config.status
)

ORUVANORUVAN = """ஒருவன் ஒருவன் முதலாளி
உலகில் மற்றவன் தொழிலாளி
விதியை நினைப்பவன் ஏமாளி
அதை வென்று முடிப்பவன் அறிவாளி

பூமியை வெல்ல ஆயுதம் எதற்கு
பூப்பறிக்க கோடரி எதற்கு
பொன்னோ பொருளோ போர்க்களம் எதற்கு
ஆசை துறந்தால் அகிலம் உனக்கு
"""


@client.event
async def on_ready():
    start_embed = discord.Embed(
        title="BOTが起動しました！",
        description="BOT has been started!",
        color=0xffd700,
        timestamp=datetime.now()
    )

    logger.info("BOTが起動しました")

    for f in config.enabled_features:
        await client.load_extension(f)
        logger.info(f"機能 [{f}] が正常にロードされました。")

    await client.tree.sync()
    await client.change_presence(activity=status)

    if config.start_notice_channel is not None:
        start_notice_channel = await client.fetch_channel(config.start_notice_channel)
        await start_notice_channel.send(embed=start_embed)


@client.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        if message.author.id in client.owner_ids or []:
            await client.process_commands(message)

    if message.author.id == config.bump.disboard_id:
        embeds = message.embeds

        if embeds is not None and len(embeds) != 0:
            if "表示順をアップしたよ" in (embeds[0].description or ""):
                JST_time = datetime.now()
                master = JST_time + timedelta(hours=2)
                fmaster = master.strftime(" %Y/%m/%d %H:%M:%S ")
                notice_channel = await client.fetch_channel(
                    config.bump.channel_id
                )

                bump_notice_embed = discord.Embed(
                    title="BUMPを検知しました",
                    description=f"次は {fmaster} 頃に通知するね～ \n ",
                    color=0x00bfff,
                    timestamp=JST_time
                )
                bump_notice_embed.add_field(
                    name="BUMP detected",
                    value=f"The next time you can BUMP is {fmaster}"
                )

                another_channel_bump_notice_embed = discord.Embed(
                    title="別のチャンネルでBUMPを検知しました",
                    description=f"次はここのチャンネルで {fmaster} 頃に通知するね～ \n ",
                    color=0x00bfff,
                    timestamp=JST_time
                )
                another_channel_bump_notice_embed.add_field(
                    name="BUMP detected on another channel",
                    value=f"The next time you can BUMP is {fmaster} in this channel"
                )

                caution_another_channel_bump_notice_embed = discord.Embed(
                    title="ここのチャンネルでBUMPしないでね",
                    description=f"次からは {notice_channel.mention} でBUMPしてね \n ",
                    color=0xff4500,
                    timestamp=JST_time
                )
                caution_another_channel_bump_notice_embed.add_field(
                    name="Don't BUMP on this channel here",
                    value=f"Next time, BUMP at {notice_channel.mention}!"
                )

                if message.channel.id != config.bump.channel_id:
                    await notice_channel.send(
                        "＼(^o^)／", embed=another_channel_bump_notice_embed
                    )
                    await message.channel.send(
                        embed=caution_another_channel_bump_notice_embed
                    )
                else:
                    await message.channel.send(
                        embed=bump_notice_embed
                    )

                client.cogs.get("BumpNofiticationCog").bump_data.last_timestamp = datetime.now().timestamp()
                client.cogs.get("BumpNofiticationCog").bump_data.notified = False

    # ----------------------------------------------------------------

    # メッセージの内容をチェック
    if "https://discord.com/channels/" in message.content:
        # メッセージリンクが含まれている場合
        try:
            link = message.content.split("https://discord.com/channels/")[1].split(" ")[0].split("\n")[0]
            guild_id, channel_id, message_id = map(int, link.split("/"))
        except Exception:
            return

        # メッセージリンクが現在のサーバーに属しているかどうかをチェック
        if message.guild.id != guild_id:
            # 現在のサーバー以外のリンクには反応しない
            return

        try:
            # リンク先のメッセージオブジェクトを取得
            target_channel = client.get_guild(guild_id).get_channel(channel_id)
            target_message = await target_channel.fetch_message(message_id)

            # リンク先のメッセージオブジェクトから、メッセージの内容、送信者の名前とアイコンなどの情報を取得
            content = target_message.content
            author = target_message.author
            name = author.name
            icon_url = author.avatar.url if author.avatar else \
                author.default_avatar.url
            timestamp = target_message.created_at
            target_message_link = \
                f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

            if content == "":
                content = "本文なし"

            # Embedオブジェクトを作成
            embed = discord.Embed(
                description=content,
                color=0x00bfff,
                timestamp=timestamp
            )
            embed.set_author(name=name, icon_url=icon_url)
            embed.set_footer(text=f"From #{target_message.channel}")

            # 画像添付ファイルがある場合、最初の画像をEmbedに追加
            if target_message.attachments:
                attachment = target_message.attachments[0]  # 最初の添付ファイルを取得
                if any(attachment.filename.lower().endswith(image_ext)
                        for image_ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    embed.set_image(url=attachment.url)  # 画像をEmbedに設定

            # ボタンコンポーネントを使ったViewオブジェクトを作成
            view = discord.ui.View(timeout=None)
            view.add_item(discord.ui.Button(
                label="メッセージ先はこちら",
                style=discord.ButtonStyle.link,
                url=target_message_link
            ))

            # EmbedとViewをメッセージとして送信
            await message.channel.send(embed=embed, view=view)

            # リンク先のメッセージがembedだった場合は、元のembedも表示する
            for original_embed in target_message.embeds:
                await message.channel.send(embed=original_embed, view=view)

        except Exception as e:
            logger.error(f"エラーらしい: {e}")

    # ----------------------------------------------------------------

    # メッセージの内容をチェック
    if message.channel.id == 965095619838488576:
        if message.author.bot:
            return

        elif message.content.startswith("ぬるぽ"):
            await message.channel.send("ｶﾞﾌﾞｯ")

        elif message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")

        elif message.content.startswith("/bump"):
            await message.channel.send(
                embed=discord.Embed(
                    title="BUMPを実行出来てないよ!!",
                    color=0x00bfff,
                    timestamp=datetime.now()
                )
            )

        elif message.content.startswith("oruvanoruvan"):
            await message.channel.send(ORUVANORUVAN)

    elif message.channel.id == config.bump.channel_id:
        if message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")

        elif message.content.startswith("/bump"):
            await message.channel.send(embed=discord.Embed(
                title="BUMPを実行出来てないよ!!",
                color=0x00bfff,
                timestamp=datetime.now())
            )

    if client.user in message.mentions and message.reference is None:
        await message.channel.send(
            f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね"
        )

# ----------------------------------------------------------------


@client.tree.error
async def on_error(ctx: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole) or isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message("権限あらへんで(関西弁)", ephemeral=True)
    else:
        print(error)

# ----------------------------------------------------------------


@client.event
async def on_close():
    logger.info("機能のアンロードを行っています...")
    for e in client.extensions.keys():
        await client.unload_extension(e)
    logger.info("機能のアンロードが完了しました。プロセスを終了します")

if config.token == "FILE":
    config.token = open("..\\CMTK.txt", mode="r").read()


async def start_setup():
    logging.config.dictConfig(yaml.load(
        await (await aiofiles.open("./data/logging.yaml")).read(),
        Loader=yaml.SafeLoader
    ))
    await setup()
    await setup_mcdata()

if __name__ == "__main__":
    asyncio.run(start_setup())


client.run(config.token, log_handler=None)
