from discord.ext import commands
from datetime import datetime
from discord import app_commands, Interaction
import discord
from database import User, session, Oregacha, session2
import random
import json

# ogint1 : cog.core_gacha.py使用中(１日のガチャによる経験値量の収支)
# ogstr1 : cog.core_gacha.py使用中(１日のガチャによる結果表示)


async def coregacha(interaction: Interaction):
    num = random.randint(1, 100000)
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()
    with open("data/json_ore_gacha.json", "r", encoding="utf-8") as f:
        jsonfile = json.load(f)
        data = jsonfile["gacha1"]

    for i, item in enumerate(data):
        if num >= item["seed_start"]:
            xp = int(item["level"]) * 10000 + int(item["xp"])
            embed = discord.Embed(
                title="ガチャ結果",
                description=f"# {item["japanese"]}\n-# ** **\nNo.{num:06}\n確率: {item["percent"]}\n経験値: {xp} XP",
                color=0xff9b37
            )
            embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
            embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + xp}XP")
            file1 = discord.File(f"assets/ore_gacha/{item["filename"]}.png", filename=f"{item["filename"]}.png")
            embed.set_thumbnail(url=f"attachment://{item["filename"]}.png")
            embed.add_field(name="本日のガチャ結果", value=f"{ogdb.ogstr1 + item["emoji"]}")
            await interaction.response.send_message(embed=embed, file=file1, silent=True)

            # 経験値等処理
            xpdb.exp += xp
            if xp < 0:
                xpdb.allremoveexp += abs(xp)
            else:
                xpdb.alladdexp += xp
            if xpdb.exp >= 10000:  # レベルアップ
                xpdb.level += 1
                xpdb.exp -= 10000
            if xpdb.exp < 0:
                xpdb.level -= 1
                xpdb.exp += 10000
            session.commit()
            ogdb.allcount += 1
            exec(f"ogdb.{item["database"]} += 1")
            ogdb.ogstr1 += item["emoji"]
            ogdb.ogint1 += xp
            alldb.allcount += 1
            exec(f"alldb.{item["database"]} += 1")
            session2.commit()
            return


async def coregacha9(interaction: Interaction):
    num = random.randint(1, 100000)
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()
    with open("data/json_ore_gacha.json", "r", encoding="utf-8") as f:
        jsonfile = json.load(f)
        data = jsonfile["gacha2"]

    for i, item in enumerate(data):
        if num >= item["seed_start"]:
            xp = int(item["level"]) * 10000 + int(item["xp"])
            embed = discord.Embed(
                title="【約９倍デー】ガチャ結果",
                description=f"# {item["japanese"]}\n-# ** **\nNo.{num:06}\n確率: {item["percent"]}\n経験値: {xp} XP",
                color=0x00f000
            )
            embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
            embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + xp}XP")
            file1 = discord.File(f"assets/ore_gacha/{item["filename"]}.png", filename=f"{item["filename"]}.png")
            embed.set_thumbnail(url=f"attachment://{item["filename"]}.png")
            embed.add_field(name="本日のガチャ結果", value=f"{ogdb.ogstr1 + item["emoji"]}")
            await interaction.response.send_message(embed=embed, file=file1, silent=True)

            # 経験値等処理
            if int(item["level"]) == 0 and int(item["xp"]) != 0:
                xpdb.exp += xp
                if xp < 0:
                    xpdb.allremoveexp += abs(xp)
                else:
                    xpdb.alladdexp += xp
                if xpdb.exp >= 10000:  # レベルアップ
                    xpdb.level += 1
                    xpdb.exp -= 10000
                if xpdb.exp < 0:
                    xpdb.level -= 1
                    xpdb.exp += 10000
                session.commit()
            elif int(item["level"]) != 0 and int(item["xp"]) == 0:
                xpdb.level += int(item["level"])
                if xp < 0:
                    xpdb.allremoveexp += abs(xp)
                else:
                    xpdb.alladdexp += xp
                session.commit()
            ogdb.allcount += 1
            exec(f"ogdb.{item["database"]} += 1")
            ogdb.ogstr1 += item["emoji"]
            ogdb.ogint1 += xp
            alldb.allcount += 1
            exec(f"alldb.{item["database"]} += 1")
            session2.commit()
            return


async def coregacha10ren(interaction: Interaction):
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()
    numberlist = []
    explist = []
    emojilist = []
    jpnamelist = []
    countlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    with open("data/json_ore_gacha.json", "r", encoding="utf-8") as f:
        jsonfile = json.load(f)
        data = jsonfile["gacha1"]

    for count in range(10):
        num = random.randint(1, 100000)
        for i, item in enumerate(data):
            if num >= item["seed_start"]:
                numberlist.append(num)
                explist.append(int(item["level"]) * 10000 + int(item["xp"]))
                emojilist.append(item["emoji"])
                jpnamelist.append(item["japanese"])
                exec(f"ogdb.{item['database']} += 1")
                alldb.allcount += 1
                exec(f"alldb.{item['database']} += 1")
                ogdb.allcount += 1
                session2.commit()
                break
    sumxp = sum(explist)
    ogdb.ogint1 += sumxp
    ogdb.ogstr1 += "".join(emojilist)
    xpdb.exp += sumxp
    if xpdb.exp >= 10000:  # レベルアップ
        xpdb.level += 1
        xpdb.exp -= 10000
    if xpdb.exp < 0:
        xpdb.level -= 1
        xpdb.exp += 10000
    session.commit()
    session2.commit()
    desc = "\n".join([f"`{count:02}` {emoji} No.{num:06} {jpname} {exp} XP" for count, emoji, jpname, num, exp in zip(countlist, emojilist, jpnamelist, numberlist, explist)])

    embed = discord.Embed(
        title="ガチャ結果【10連】",
        description=desc,
        color=0xff9b37
    )
    embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
    embed.set_footer(text=f"本日残り: 0回 / 今日の収支: {sumxp}XP")

    await interaction.response.send_message(embed=embed, silent=True)


class COregacha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="core-gacha", description="鉱石ガチャコマンド")
    async def coregachacom(self, interaction: discord.Interaction):
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        gachadb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
        if not userdb:
            session.add(User(userid=interaction.user.id, username=interaction.user.name))
            session.commit()
            await interaction.response.send_message("経験値データベースにユーザーを登録しました\nもう一度実行してください(1日あたりの実行回数は減りません)\nなお、まだ一度もガチャをしていない人は次の実行でガチャデータベースにユーザー登録されます", ephemeral=True)
            return
        if not gachadb:
            session2.add(Oregacha(userid=interaction.user.id, username=interaction.user.name, ogstr1=""))
            session2.commit()
            await interaction.response.send_message("ガチャデータベースにユーザーを登録しました\nもう一度実行してください(1日あたりの実行回数は減りません)\n次でガチャが回せるはずです", ephemeral=True)
            return
        if userdb.noxp is True:
            await interaction.response.send_message("あなたは経験値システムが無効化されてるからガチャを回せません", ephemeral=True)
            return
        if gachadb.dailygacha >= 10:
            await interaction.response.send_message(f"本日のガチャ回数が上限に達しました\nまた明日回してね(^^♪\n-# 00:00:00～00:01:00に更新されます\n本日の収支は{gachadb.ogint1}XPでした", ephemeral=True)
            return
        now = datetime.now()
        if now.day == 9:
            gachadb.dailygacha += 1
            session2.commit()
            await coregacha9(interaction)
        elif now.day == 22 and now.month == 7:
            gachadb.dailygacha += 1
            session2.commit()
            await coregacha9(interaction)
        else:
            gachadb.dailygacha += 1
            session2.commit()
            await coregacha(interaction)

    # @app_commands.command(name="core", description="鉱石ガチャ登録")
    # async def coregachatouroku(self, interaction: discord.Interaction):
    #     session2.add(Oregacha(userid=101, username="合計"))
    #     session2.commit()
    #     await interaction.response.send_message("合計データを登録しました", ephemeral=True)

    @app_commands.command(name="core-gacha-10", description="鉱石ガチャコマンド【10連】")
    async def coregacha10renncom(self, interaction: discord.Interaction):
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        gachadb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
        if not userdb:
            session.add(User(userid=interaction.user.id, username=interaction.user.name))
            session.commit()
            await interaction.response.send_message("経験値データベースにユーザーを登録しました\nもう一度実行してください(1日あたりの実行回数は減りません)\nなお、まだ一度もガチャをしていない人は次の実行でガチャデータベースにユーザー登録されます", ephemeral=True)
        elif not gachadb:
            session2.add(Oregacha(userid=interaction.user.id, username=interaction.user.name, ogstr1=""))
            session2.commit()
            await interaction.response.send_message("ガチャデータベースにユーザーを登録しました\nもう一度実行してください(1日あたりの実行回数は減りません)\n次でガチャが回せるはずです", ephemeral=True)
        elif userdb.noxp is True:
            await interaction.response.send_message("あなたは経験値システムが無効化されてるからガチャを回せません", ephemeral=True)
        elif gachadb.dailygacha > 0:
            await interaction.response.send_message(f"本日既に{gachadb.dailygacha}回ガチャを回しているため、10連は回せません\n本日の収支は{gachadb.ogint1}XPでした", ephemeral=True)
        else:
            now = datetime.now()
            if now.day == 22 and now.month == 7:
                await interaction.response.send_message("本日は周年期間中の為10連ガチャを回すことができません\n通常ガチャを回してください", ephemeral=True)
                return
            elif now.day != 9:
                gachadb.dailygacha += 10
                session2.commit()
                await coregacha10ren(interaction)
            else:
                await interaction.response.send_message("毎月9日は10連ガチャを回すことができません\n通常ガチャを回してください", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(COregacha(bot))
