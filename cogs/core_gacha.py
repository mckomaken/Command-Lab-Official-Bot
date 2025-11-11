from discord.ext import commands
from datetime import datetime
from discord import app_commands, Interaction
import discord
from database import User, session, Oregacha, session2
import random
import json

# ogint1 : cog.core_gacha.py使用中(１日のガチャによる経験値量の収支)
# ogstr1 : cog.core_gacha.py使用中(１日のガチャによる結果表示)


async def cOreGacha(interaction: Interaction):
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


async def cOreGacha9(interaction: Interaction):
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
            ogdb.ogint2 += 1
            exec(f"ogdb.{item["database"]} += 1")
            ogdb.ogstr1 += item["emoji"]
            ogdb.ogint1 += xp
            alldb.ogint2 += 1
            exec(f"alldb.{item["database"]} += 1")
            session2.commit()
            return


async def cOreGacha10(interaction: Interaction):
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()
    numberlist = []
    explist = []
    emojilist = []
    jpnamelist = []
    countlist = []
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
                countlist.append(count + 1)
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
    desc = "\n".join([f"`{count:02}` {emoji} `No.{num:06}` {jpname} {exp} XP" for count, emoji, jpname, num, exp in zip(countlist, emojilist, jpnamelist, numberlist, explist)])

    if sumxp >= 3456:
        embed = discord.Embed(
            title="10連ガチャ結果 : 最高記録更新！",
            description=desc,
            color=0x9224ff
        )
        # https://discord.com/channels/735130420630388807/965095619838488576/1416628799638081656
    elif sumxp >= 2000:
        embed = discord.Embed(
            title="10連ガチャ結果 : 大当たり",
            description=desc,
            color=0x80ff80
        )
    elif sumxp >= 1000:
        embed = discord.Embed(
            title="10連ガチャ結果 : 中当たり",
            description=desc,
            color=0xffff00
        )
    elif sumxp >= 800:
        embed = discord.Embed(
            title="10連ガチャ結果 : 当たり",
            description=desc,
            color=0xff9b37
        )
    elif sumxp >= 0:
        embed = discord.Embed(
            title="10連ガチャ結果 : はずれ",
            description=desc,
            color=0xf36d4b
        )
    elif sumxp >= -531:
        embed = discord.Embed(
            title="10連ガチャ結果 : 大はずれ",
            description=desc,
            color=0x400000
        )
    else:
        embed = discord.Embed(
            title="10連ガチャ結果 : 最低記録更新！",
            description=desc,
            color=0xff0000
        )
        # https://discord.com/channels/735130420630388807/965095619838488576/1382557452893163632
    embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
    embed.set_footer(text=f"本日残り: 0回 / 今日の収支: {sumxp}XP")

    await interaction.response.send_message(embed=embed, silent=True)


class COregacha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="core-gacha", description="鉱石ガチャコマンド")
    async def cOreGachaCommand(self, interaction: discord.Interaction):
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
            await cOreGacha9(interaction)
        elif now.day == 21 and now.month == 7:
            gachadb.dailygacha += 1
            session2.commit()
            await cOreGacha9(interaction)
        else:
            gachadb.dailygacha += 1
            session2.commit()
            await cOreGacha(interaction)

    # @app_commands.command(name="core", description="鉱石ガチャ登録")
    # async def coregachatouroku(self, interaction: discord.Interaction):
    #     session2.add(Oregacha(userid=101, username="合計"))
    #     session2.commit()
    #     await interaction.response.send_message("合計データを登録しました", ephemeral=True)

    @app_commands.command(name="core-gacha-10", description="鉱石ガチャコマンド【10連】")
    async def cOreGacha10Command(self, interaction: discord.Interaction):
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
                await cOreGacha10(interaction)
            else:
                await interaction.response.send_message("毎月9日は10連ガチャを回すことができません\n通常ガチャを回してください", ephemeral=True)

    @app_commands.command(name="core-gacha-list", description="鉱石ガチャ結果一覧")
    @app_commands.describe(server="サーバー全体の確率表示(未指定:FALSE(自分の結果表示))")
    async def cOreGachaListCommand(self, interaction: discord.Interaction, server: bool = False):
        if server is False:
            gachadb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
            if not gachadb:
                await interaction.response.send_message("あなたはまだ一度もガチャを回していないため、結果を見ることができません\nまずはガチャを回してください", ephemeral=True)
                return
            with open("data/json_ore_gacha.json", "r", encoding="utf-8") as f:
                jsonfile = json.load(f)
                data1 = jsonfile["gacha1"]
                data2 = jsonfile["gacha2"]
            desc = ""
            for item in data1:
                count = eval(f"gachadb.{item['database']}")
                persent = (count / gachadb.allcount * 100) if gachadb.allcount > 0 else 0
                desc += f"{item['emoji']} : `{count:03}`回 `{persent:09.06f}`%\n"
            desc += "------------------\n"
            for item in data2:
                count = eval(f"gachadb.{item['database']}")
                persent = (count / gachadb.ogint2 * 100) if gachadb.allcount > 0 else 0
                desc += f"{item['emoji']} : `{count:03}`回 `{persent:09.06f}`%\n"
            desc += "------------------\n"
            desc += f"通常合計: {gachadb.allcount}回 ・ 約9倍デー合計: {gachadb.ogint2}回"
            embed = discord.Embed(
                title=f"{interaction.user.display_name}さんのガチャ結果",
                description=desc,
                color=0x00aaff
            )
            embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, silent=True)
        else:
            alldb = session2.query(Oregacha).filter_by(userid="101").first()
            with open("data/json_ore_gacha.json", "r", encoding="utf-8") as f:
                jsonfile = json.load(f)
                data1 = jsonfile["gacha1"]
                data2 = jsonfile["gacha2"]
            desc = ""
            for item in data1:
                count = eval(f"alldb.{item['database']}")
                persent = (count / alldb.allcount * 100) if alldb.allcount > 0 else 0
                desc += f"{item['emoji']} : `{count:04}`回 `{persent:09.06f}`%\n"
            desc += "------------------\n"
            for item in data2:
                count = eval(f"alldb.{item['database']}")
                persent = (count / alldb.ogint2 * 100) if alldb.allcount > 0 else 0
                desc += f"{item['emoji']} : `{count:04}`回 `{persent:09.06f}`%\n"
            desc += "------------------\n"
            desc += f"通常合計: {alldb.allcount}回 ・ 約9倍デー合計: {alldb.ogint2}回"
            embed = discord.Embed(
                title="サーバー全体のガチャ結果",
                description=desc,
                color=0x00aaff
            )
            embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(COregacha(bot))
