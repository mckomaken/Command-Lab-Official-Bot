import os
import discord
import uuid
import logging

from typing import Optional
from discord.ext import commands
from datetime import datetime, timedelta
from discord import app_commands
from config import config
from util import create_codeblock

client = commands.Bot(intents=discord.Intents.all(), command_prefix="cm!")
logger = logging.getLogger("root")
txt = discord.Embed


status = discord.Activity(
    type=discord.ActivityType.playing,
    name=config.status
)


class SampleView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)


@client.event
async def on_ready():
    SJST_time = datetime.now()
    start_embed = discord.Embed(
        title="BOTが起動しました！",
        description="BOT has been started!",
        color=0xffd700,
        timestamp=SJST_time
    )

    logger.info("BOTが起動しました")

    for f in config.enabled_features:
        await client.load_extension(f)
    await client.load_extension("jishaku")

    await client.tree.sync()
    await client.change_presence(activity=status)

    if config.start_notice_channel is not None:
        start_notice_channel = await client.fetch_channel(config.start_notice_channel)
        await start_notice_channel.send(embed=start_embed)


@client.event
async def on_message(message: discord.Message):
    if message.author.id == config.bump.disboard_id:
        embeds = message.embeds

        if embeds is not None and len(embeds) != 0:
            if "表示順をアップしたよ" in embeds[0].description:
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

    # ----------------------------------------------------------------

    # メッセージの内容をチェック
    if "https://discord.com/channels/" in message.content:
        # メッセージリンクが含まれている場合
        try:
            link = message.content.split("https://discord.com/channels/")[1]
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
            view = SampleView(timeout=None)
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
            await message.channel.send("ஒருவன் ஒருவன் முதலாளி\nஉலகில் மற்றவன் தொழிலாளி\nவிதியை நினைப்பவன் ஏமாளி\nஅதை வென்று முடிப்பவன் அறிவாளி\n \nபூமியை வெல்ல ஆயுதம் எதற்கு\nபூப்பறிக்க கோடரி எதற்கு\nபொன்னோ பொருளோ போர்க்களம் எதற்கு\nஆசை துறந்தால் அகிலம் உனக்கு")

    elif message.channel.id == config.bump.channel_id:
        if message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")

        elif message.content.startswith("/bump"):
            await message.channel.send(embed=discord.Embed(
                title="BUMPを実行出来てないよ!!",
                color=0x00bfff,
                timestamp=datetime.now())
            )

    if client.user in message.mentions:
        await message.channel.send(
            f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね"
        )

# ----------------------------------------------------------------


@client.tree.command(name="cmennte", description="【運営】各種お知らせ用")
@app_commands.describe(
    title="タイトル",
    description="説明",
    sub_title="サブタイトル",
    sub_description="サブ説明"
)
@app_commands.checks.has_permissions(
    manage_guild=True
)
async def cmennte(
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
    mennte_embed.add_field(
        name=sub_title,
        value=sub_description,
    )

    await interaction.response.send_message(embed=mennte_embed)

# ----------------------------------------------------------------


@client.tree.command(name="cl", description="【運営】運営専用雑コマンド")
@app_commands.describe(
    choice="選択肢",
)
@app_commands.choices(
    choice=[
        app_commands.Choice(name="高校おめ", value="cl1"),
        app_commands.Choice(name="大学おめ", value="cl2")
    ]
)
async def cl(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    role = interaction.guild.get_role(config.administrater_role_id)
    if role in interaction.user.roles:
        if choice.value == "cl1":
            await interaction.response.send_message(embed=discord.Embed(
                title="高校合格おめでとうございます!!", color=0x2b9788
            ))
        elif choice.value == "cl2":
            await interaction.response.send_message(embed=discord.Embed(
                title="大学合格おめでとうございます!!", color=0x2b9788
            ))

# ----------------------------------------------------------------


@client.tree.command(
    name="cuuid", description="UUIDを生成します"
)
@app_commands.describe(
    count="生成する量(デフォルト: 2)"
)
async def cuuid(interaction: discord.Interaction, count: Optional[app_commands.Range[int, 1, 25]] = 2):
    uuJST_time = datetime.now()

    uuid_embed = discord.Embed(
        title="UUID Generator",
        description=f"-----------------------------------------------------\n{count}個のUUIDを自動生成しました\nBEのAdd-on制作にお役立てください\n-----------------------------------------------------",
        color=0x58619a,
        timestamp=uuJST_time
    )

    for i in range(count):
        uuid2 = str(uuid.uuid4())
        uuid2_nosep = uuid2.replace("-", "")

        uuid_embed.add_field(name=f"{i + 1}個目", value=f"{create_codeblock(uuid2)}\n{create_codeblock(uuid2_nosep)}")

    await interaction.response.send_message(embed=uuid_embed)

# ----------------------------------------------------------------


@client.tree.command(name="cping", description="pingを計測します")
async def cping(interaction: discord.Interaction):

    piJST_time = datetime.now()
    text = f'{round(client.latency*1000)}ms'

    ping_embed = discord.Embed(
        title="現在のping",
        description=text,
        timestamp=piJST_time
    )

    await interaction.response.send_message(embed=ping_embed)

# ----------------------------------------------------------------


@client.tree.command(name="chelp", description="このBotができること一覧")
async def chelp(interaction: discord.Interaction):

    chJST_time = datetime.now()

    chelp_embed = discord.Embed(
        title="コマンド一覧",
        description="/chelp : この説明文が出てきます\n/cping : サーバーとBotとのping値を測定できます\n/cuuid : 2個のUUIDを自動生成してくれます\n/cpack-mcmeta : ResourcePackとDataPackのpack_formatの番号一覧を表示します",
        color=0x2b9900,
        timestamp=chJST_time
    )

    await interaction.response.send_message(embed=chelp_embed)

# ----------------------------------------------------------------


@client.tree.error
async def on_error(ctx: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole) or isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message("権限あらへんで(関西弁)", ephemeral=True)


# ----------------------------------------------------------------


if not os.path.exists("./tmp/bump_data.json"):
    open("./tmp/bump_data.json").write(BumpData.model_dump_json())

# ----------------------------------------------------------------


client.run(config.token)
