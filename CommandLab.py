import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from discord.ui import View , Button
from discord import Client, Intents, Interaction, app_commands

client = commands.Bot(intents=discord.Intents.all(), command_prefix="cm!")
txt = discord.Embed


status = discord.Activity(type=discord.ActivityType.playing, name="コマンドとPythonを勉強中")

class SampleView(discord.ui.View): 
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

@client.event
async def on_ready():
    
    start_notice_channel = await client.fetch_channel(965098244193542154) #965098244193542154 # <-コマ研DISBORD用チャンネル
    SJST_time = datetime.now()
    start_embed = discord.Embed(
        title="BOTが起動しました！", 
        description=f"なお起動後のBUMPは通知されないので自分で2時間計ってBUMPしてください！ \n ", 
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
    #await start_notice_channel.send(embed=start_embed)

@client.event
async def on_message(message):
    if message.author.id == 302050872383242240: #302050872383242240: # <-DISBORD ID
        embeds = message.embeds
            
        if embeds is not None and len(embeds) != 0:
            if "表示順をアップしたよ" in embeds[0].description:
                JST_time = datetime.now()
                master = JST_time + timedelta(hours=2)
                fmaster = master.strftime(" %Y/%m/%d %H:%M:%S ")
                notice_channel = await client.fetch_channel(965098244193542154) #965098244193542154 # <-コマ研DISBORD用チャンネル
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
                    value=f"It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
                    )
                bump_embed.set_image(url="attachment://bump.png")

                if message.channel.id == 965098244193542154: #965098244193542154 # <-コマ研DISBORD用チャンネル
                    await message.channel.send("＼(^o^)／", embed = bump_notice_embed)
                    await asyncio.sleep(7200) # 7200に変更すること
                    await message.channel.send("BUMP TIME !!", file=bump_file, embed = bump_embed)

                else:
                    await notice_channel.send("＼(^o^)／", embed = another_channel_bump_notice_embed)
                    await message.channel.send(embed = caution_another_channel_bump_notice_embed)
                    await asyncio.sleep(7200) # 7200に変更すること
                    await notice_channel.send("BUMP TIME !!", file=bump_file, embed = bump_embed)

        #----------------------------------------------------------------

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
            icon_url = author.avatar.url if author.avatar else author.default_avatar.url
            timestamp = target_message.created_at
            target_message_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

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
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    embed.set_image(url=attachment.url)  # 画像をEmbedに設定


            # ボタンコンポーネントを使ったViewオブジェクトを作成
            view = SampleView(timeout=None)
            view.add_item(discord.ui.Button(label="メッセージ先はこちら", style=discord.ButtonStyle.link, url=target_message_link))

            # EmbedとViewをメッセージとして送信
            await message.channel.send(embed=embed, view=view)

            # リンク先のメッセージがembedだった場合は、元のembedも表示する
            for original_embed in target_message.embeds:
                await message.channel.send(embed=original_embed, view=view)

        except Exception as e:
            print(f"エラーらしい: {e}")

#----------------------------------------------------------------

#@client.tree.command(name="testbump", description="【運営】テスト用Bumpコマンド")
#@discord.app_commands.checks.has_role("運営")
#async def testbump(interaction: discord.Interaction):
#    embeds = discord.Embed(
#        title="BumpTest",
#        color=0xff1948,
#        description="表示順をアップしたよ:thumbsup:"
#    )
#    await interaction.response.send_message(embed=embeds)

#----------------------------------------------------------------

@client.tree.command(name="bnoticetime", description="【運営】再起動後の通知時間設定用")
#@discord.app_commands.checks.has_role("運営")
@discord.app_commands.describe(
    addminutes="入力分後に通知されます"
)
async def bnoticetime(interaction: discord.Interaction, addminutes: int):
        role = interaction.guild.get_role(735130783760777270) #735130783760777270<-コマ研運営のロールID貼ること
        if role in interaction.user.roles: #<-上記のロールを持っていたら
            bnJST_time = datetime.now()
            ScheduledTime = bnJST_time + timedelta(minutes=addminutes)
            fScheduledTime = ScheduledTime.strftime(" %Y/%m/%d %H:%M ")
            notice_channel = await client.fetch_channel(965098244193542154) #965098244193542154 # <-コマ研DISBORD用チャンネル
            bump_file = discord.File("bump.png", filename="bump.png")

            bump_embed = discord.Embed(
                title="BUMPの時間だよ(^O^)／", 
                description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ", 
                color=0x00ffff,
                timestamp=ScheduledTime
                )
            bump_embed.add_field(
                name="It's BUMP time (^O^)/", 
                value=f"It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
                )
            bump_embed.set_image(url="attachment://bump.png")

            await interaction.response.send_message(f"{addminutes}分後({fScheduledTime}頃)に通知されます")
            await asyncio.sleep(addminutes*60)
            await notice_channel.send("BUMP TIME !!", file=bump_file, embed = bump_embed)

        else: #<-上記のロールを持っていなかったら
            await interaction.response.send_message("JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}" , ephemeral=True)

#----------------------------------------------------------------

@client.tree.command(name="mennte", description="【運営】各種お知らせ用")
@discord.app_commands.describe(
    daimei="タイトル",
    setumei="説明",
    subdaimei="サブタイトル",
    subsetumei="サブ説明"
)
async def mennte(interaction: discord.Interaction, daimei: str, setumei: str, subdaimei: str = "", subsetumei: str = ""):
        role = interaction.guild.get_role(735130783760777270) #<-コマ研運営のロールID貼ること
        if role in interaction.user.roles: #<-上記のロールを持っていたら

            mntJST_time = datetime.now()

            mennte_embed = discord.Embed(
                title=daimei, 
                description=setumei, 
                color=0xff580f,
                timestamp=mntJST_time
                )
            mennte_embed.add_field(
                name=subdaimei,
                value=subsetumei,
                )
            
            await interaction.response.send_message(embed = mennte_embed)

        else: #<-上記のロールを持っていなかったら
            await interaction.response.send_message("JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}" , ephemeral=True)

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
        description="/chelp : この説明文が出てきます\n/ping : サーバーとBotとのping値を測定できます", 
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









