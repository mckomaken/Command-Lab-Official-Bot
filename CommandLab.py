import discord
import asyncio
import uuid

from discord.ext import commands
from datetime import datetime, timedelta
from discord import app_commands
from config import config

client = commands.Bot(intents=discord.Intents.all(), command_prefix="cm!")
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
    start_notice_channel = await client.fetch_channel(config.bump.channel_id)
    SJST_time = datetime.now()
    start_embed = discord.Embed(
        title="BOTが起動しました！",
        description="なお起動後のBUMPは通知されないので自分で2時間計ってBUMPしてください！ \n ",
        color=0xffd700,
        timestamp=SJST_time
        )
    start_embed.add_field(
        name="BOT has been activated!",
        value=f"You should measure 2 hours and BUMP by yourself because you are not notified of the BUMP after startup!"
        )

    print("BOTが起動しました")
    await client.tree.sync()
    await client.change_presence(activity=status)
    # await start_notice_channel.send(embed=start_embed)

@client.event
async def on_message(message: discord.Message):
    if message.author.id == config.bump.disboard_id:
        # 302050872383242240 <-DISBORD ID
        embeds = message.embeds

        if embeds is not None and len(embeds) != 0:
            if "表示順をアップしたよ" in embeds[0].description:
                JST_time = datetime.now()
                master = JST_time + timedelta(hours=2)
                fmaster = master.strftime(" %Y/%m/%d %H:%M:%S ")
                notice_channel = await client.fetch_channel(
                    config.bump.channel_id
                )
                # 965098244193542154 # <-コマ研DISBORD用チャンネル
                bump_file = discord.File("bump.png", filename="bump.png")

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

                bump_embed = discord.Embed(
                    title="BUMPの時間だよ(^O^)／",
                    description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
                    color=0x00ffff,
                    timestamp=master
                )
                bump_embed.add_field(
                    name="It's BUMP time (^O^)/",
                    value="It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
                )
                bump_embed.set_image(url="attachment://bump.png")

                if message.channel.id == config.bump.channel_id:
                    # 965098244193542154 <-コマ研DISBORD用チャンネル
                    await message.channel.send(
                        "＼(^o^)／", embed=bump_notice_embed
                    )
                    await asyncio.sleep(7200)       # 7200に変更すること
                    await message.channel.send(
                        "BUMP TIME !!", file=bump_file, embed=bump_embed
                    )

                else:
                    await notice_channel.send(
                        "＼(^o^)／", embed=another_channel_bump_notice_embed
                    )
                    await message.channel.send(
                        embed=caution_another_channel_bump_notice_embed
                    )
                    await asyncio.sleep(7200)       # 7200に変更すること
                    await notice_channel.send(
                        "BUMP TIME !!", file=bump_file, embed=bump_embed
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
            print(f"エラーらしい: {e}")
    # ----------------------------------------------------------------

    # メッセージの内容をチェック
    if message.channel.id == 965095619838488576:
        if message.author.bot:
            pass
        elif message.content.startswith("ぬるぽ"):
            await message.channel.send("ｶﾞﾌﾞｯ")

        elif client.user in message.mentions:
            await message.channel.send(
                f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね"
            )

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

    elif message.channel.id == 965098244193542154:
        if message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")

        elif message.content.startswith("/bump"):
            await message.channel.send(embed=discord.Embed(
                title="BUMPを実行出来てないよ!!",
                color=0x00bfff,
                timestamp=datetime.now())
            )

        elif client.user in message.mentions:
            await message.channel.send(
                f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね"
            )
    else:
        if client.user in message.mentions:
            await message.channel.send(
                f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね"
            )

# ----------------------------------------------------------------

# @client.tree.command(name="testbump", description="【運営】テスト用Bumpコマンド")
# @discord.app_commands.checks.has_role("運営")
# async def testbump(interaction: discord.Interaction):
#     embeds = discord.Embed(
#         title="BumpTest",
#         color=0xff1948,
#         description="表示順をアップしたよ:thumbsup:"
#     )
#     await interaction.response.send_message(embed=embeds)

# ----------------------------------------------------------------


@client.tree.command(name="cbnoticetime", description="【運営】再起動後の通知時間設定用")
@discord.app_commands.describe(
    addminutes="入力分後に通知されます"
)
async def cbnoticetime(interaction: discord.Interaction, addminutes: int):
    role = interaction.guild.get_role(config.administrater_role_id)
    # 735130783760777270 <- コマ研運営のロールID貼ること
    if role in interaction.user.roles:
        # <- 上記のロールを持っていたら
        bnJST_time = datetime.now()
        ScheduledTime = bnJST_time + timedelta(minutes=addminutes)
        fScheduledTime = ScheduledTime.strftime(" %Y/%m/%d %H:%M ")
        notice_channel = await client.fetch_channel(965098244193542154)
        # 965098244193542154 # <-コマ研DISBORD用チャンネル
        bump_file = discord.File("bump.png", filename="bump.png")

        bump_embed = discord.Embed(
            title="BUMPの時間だよ(^O^)/",
            description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
            color=0x00ffff,
            timestamp=ScheduledTime
            )
        bump_embed.add_field(
            name="It's BUMP time (^O^)/",
            value=f"It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
            )
        bump_embed.set_image(url="attachment://bump.png")

        await interaction.response.send_message(
            f"{addminutes}分後({fScheduledTime}頃)に通知されます"
        )
        await asyncio.sleep(addminutes*60)
        await notice_channel.send(
            "BUMP TIME !!", file=bump_file, embed=bump_embed
        )

    else:           # <-上記のロールを持っていなかったら
        await interaction.response.send_message(
            "JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}",
            ephemeral=True
        )


# ----------------------------------------------------------------

@client.tree.command(name="cmennte", description="【運営】各種お知らせ用")
@discord.app_commands.describe(
    title="タイトル",
    description="説明",
    sub_title="サブタイトル",
    sub_description="サブ説明"
)
async def cmennte(
    interaction: discord.Interaction,
    title: str,
    description: str,
    sub_title: str = "",
    sub_description: str = ""
):
    role = interaction.guild.get_role(config.administrater_role_id)
    if role in interaction.user.roles:

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

    else:
        await interaction.response.send_message("JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}" , ephemeral=True)

# ----------------------------------------------------------------


@client.tree.command(name="cl", description="【運営】運営専用雑コマンド")
@discord.app_commands.describe(
    choice="選択肢",
)
@discord.app_commands.choices(
    choice=[
        discord.app_commands.Choice(name="高校おめ", value="cl1"),
        discord.app_commands.Choice(name="大学おめ", value="cl2")
    ]
)
async def cl(interaction: discord.Interaction, choice: discord.app_commands.Choice[str]):
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


@client.tree.command(name="cuuid", description="マイクラで使えるUUIDを2個生成します")
async def cuuid(interaction: discord.Interaction):

    uuJST_time = datetime.now()
    Uuuid4 = uuid.uuid4()
    fUuuid4 = str(Uuuid4).split("-")
    cUuuid4 = fUuuid4[0]+fUuuid4[1]+fUuuid4[2]+fUuuid4[3]+fUuuid4[4]
    UUuuid4 = uuid.uuid4()
    fUUuuid4 = str(UUuuid4).split("-")
    cUUuuid4 = fUUuuid4[0]+fUUuuid4[1]+fUUuuid4[2]+fUUuuid4[3]+fUUuuid4[4]

    uuid_embed = discord.Embed(
            title="UUID Generator",
            description="-----------------------------------------------------\n2個のUUIDを自動生成しました\nBEのAdd-on制作にお役立てください\n-----------------------------------------------------",
            color=0x58619a,
            timestamp=uuJST_time
            )
    uuid_embed.add_field(
            name="１個目",
            value=f"ハイフンあり\n```{Uuuid4}```\nハイフンなし\n```{cUuuid4}```\n ",
            inline=False
            )
    uuid_embed.add_field(
            name="-----------------------------------------------------",
            value=" ",
            inline=False
            )
    uuid_embed.add_field(
            name="2個目",
            value=f"ハイフンあり\n```{UUuuid4}```\nハイフンなし\n```{cUUuuid4}```\n ",
            inline=False
            )

    await interaction.response.send_message(embed=uuid_embed)

# ----------------------------------------------------------------


@client.tree.command(
    name="cpack-mcmeta",
    description="pack.mcmetaで使われるpack_formatの番号一覧です"
)
@discord.app_commands.describe(choice="選択してください")
@discord.app_commands.choices(
    choice=[
        discord.app_commands.Choice(name="ALL-ResourcePack", value="a_respack"),
        discord.app_commands.Choice(name="ALL-DataPack", value="a_dpack"),
        discord.app_commands.Choice(name="Search-pack_format", value="spf")
    ]
)
@discord.app_commands.describe(
    version="調べたいバージョンを半角英数字で記入してください(スナップショット非対応)",
)






#----------------------------------------------------------------


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

#----------------------------------------------------------------

@client.tree.command(name="chelp", description="このBotができること一覧")
async def chelp(interaction: discord.Interaction):

    chJST_time = datetime.now()

    chelp_embed = discord.Embed(
        title="コマンド一覧",
        description="/chelp : この説明文が出てきます\n/cping : サーバーとBotとのping値を測定できます\n/cuuid : 2個のUUIDを自動生成してくれます\n/cpack-mcmeta : ResourcePackとDataPackのpack_formatの番号一覧を表示します",
        color=0x2b9900,
        timestamp=chJST_time
    )

    await interaction.response.send_message(embed = chelp_embed)

#----------------------------------------------------------------

@client.tree.error
async def on_error(ctx, error):
    if isinstance(error, app_commands.MissingRole):
        await ctx.response.send_message("権限あらへんで(関西弁)", ephemeral=True)

#----------------------------------------------------------------

with open("CMTK.txt") as file:
    client.run(file.read())

#画面上：表示⇒ターミナル、押すと実行するための画面出てくる
#実行コマンド1：cd Desktop\DiscordBot_Command_Lab_Official_Bot\Command-Lab-Official-Bot
#実行コマンド2：py .\CommandLab.py
#Botを止めるときは「Ctrl+C」を押す









