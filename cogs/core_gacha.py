from discord.ext import commands
from datetime import datetime
from discord import app_commands, Interaction
import discord
from database import User, session, Oregacha, session2
import random

# ogint1 : cog.core_gacha.py使用中(１日のガチャによる経験値量の収支)

# numの最大値
seed_max = 100000
# レベルアップに必要な経験値
required_xp = 10000

# 通常ガチャのルートテーブル
root_table = [
    {
        "seed_start":100000,
        "japanese":"ネザライトインゴット",
        "filename":"netherite_ingot",
        "xp":2200
    },
    {
        "seed_start":99914,
        "japanese":"ネザライトの欠片",
        "filename":"netherite_scrap",
        "xp":400
    },
    {
        "seed_start":99003,
        "japanese":"ラピスラズリ",
        "filename":"rapis_lazuli",
        "xp":180
    },
    {
        "seed_start":93117,
        "japanese":"ダイヤモンド",
        "filename":"diamond",
        "xp":250
    },
    {
        "seed_start":87222,
        "japanese":"金のインゴット",
        "filename":"gold_ingot",
        "xp":150
    },
    {
        "seed_start":81083,
        "japanese":"レッドストーン",
        "filename":"redstone",
        "xp":130
    },
    {
        "seed_start":73458,
        "japanese":"エメラルド",
        "filename":"emerald",
        "xp":100
    },
    {
        "seed_start":62867,
        "japanese":"鉄のインゴット",
        "filename":"iron_ingot",
        "xp":85
    },
    {
        "seed_start":51306,
        "japanese":"銅のインゴット",
        "filename":"copper_ingot",
        "xp":40
    },
    {
        "seed_start":35157,
        "japanese":"ネザークォーツ",
        "filename":"nether_quartz",
        "xp":55
    },
    {
        "seed_start":20596,
        "japanese":"石炭",
        "filename":"coal",
        "xp":80
    },
    {
        "seed_start":8851,
        "japanese":"壊れかけのツルハシ",
        "filename":"breaking_pickaxe",
        "xp":-100
    },
    {
        "seed_start":957,
        "japanese":"壊れたツルハシ",
        "filename":"broken_pickaxe",
        "xp":-400
    },
    {
        "seed_start":5,
        "japanese":"死亡",
        "filename":"death",
        "xp":-1111
    },
]

async def coregacha(interaction: Interaction):
    num = random.randint(1, seed_max) # ←これを便宜上「seed」と呼ぶことがある
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()

    def send_embed(description, xp, filename):
        embed = discord.Embed(
            title="ガチャ結果",
            description=description,
            color=0xff9b37
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + xp}XP")
        file = discord.File(f"assets/ore_gacha/{filename}.png", filename=f"{filename}.png")
        embed.set_thumbnail(url=f"attachment://{filename}.png")
        return embed, file

    for i, item in enumerate(root_table):
        if item["seed_start"] >= num:

            seed_start = item["seed_start"]
            xp = item["xp"]
            
            if i == len(root_table)-1: # もし「死亡」なら
                probability = seed_start/seed_max
            else: # そうでないなら、次のitemとのseed_startの差を取って確率を求める
                probability = (seed_start - root_table[i+1]["seed_start"])/seed_max

            # ガチャ結果送信
            embed, file = send_embed(
            f"# {item["japanese"]}\n-# ** **\nNo.{num:06}\n確率: {round(probability)}%\n経験値: {item["xp"]} XP",
            xp,
            item["filename"]
            )
            await interaction.response.send_message(embed=embed, file=file, silent=True)

            # 経験値等処理
            xpdb.exp += xp
            xpdb.alladdexp += xp
            if xpdb.exp >= required_xp: # レベルアップ
                xpdb.level += 1
                xpdb.exp -= required_xp
            session.commit()

            return


    if num >= 99915:
        ogdb.allcount += 1
        ogdb.netheritei += 1
        alldb.allcount += 1
        alldb.netheritei += 1
        ogdb.ogint1 += 2200
        session2.commit()
        return

    elif num >= 99004:
        ogdb.allcount += 1
        ogdb.netherites += 1
        alldb.allcount += 1
        alldb.netherites += 1
        ogdb.ogint1 += 400
        session2.commit()
        return

    elif num >= 93118:
        ogdb.allcount += 1
        ogdb.lapis += 1
        alldb.allcount += 1
        alldb.lapis += 1
        ogdb.ogint1 += 180
        session2.commit()
        return

    elif num >= 87223:
        ogdb.allcount += 1
        ogdb.diamond += 1
        alldb.allcount += 1
        alldb.diamond += 1
        ogdb.ogint1 += 250
        session2.commit()
        return

    elif num >= 81084:
        ogdb.allcount += 1
        ogdb.gold += 1
        alldb.allcount += 1
        alldb.gold += 1
        ogdb.ogint1 += 150
        session2.commit()
        return

    elif num >= 73459:
        ogdb.allcount += 1
        ogdb.redstone += 1
        alldb.allcount += 1
        alldb.redstone += 1
        ogdb.ogint1 += 130
        session2.commit()
        return

    elif num >= 62868:
        ogdb.allcount += 1
        ogdb.emerald += 1
        alldb.allcount += 1
        alldb.emerald += 1
        ogdb.ogint1 += 100
        session2.commit()
        return

    elif num >= 51307:
        ogdb.allcount += 1
        ogdb.iron += 1
        alldb.allcount += 1
        alldb.iron += 1
        ogdb.ogint1 += 85
        session2.commit()
        return

    elif num >= 35158:
        ogdb.allcount += 1
        ogdb.copper += 1
        alldb.allcount += 1
        alldb.copper += 1
        ogdb.ogint1 += 40
        session2.commit()
        return

    elif num >= 20597:
        ogdb.allcount += 1
        ogdb.quartz += 1
        alldb.allcount += 1
        alldb.quartz += 1
        ogdb.ogint1 += 55
        session2.commit()
        return

    elif num >= 8852:
        ogdb.allcount += 1
        ogdb.coal += 1
        alldb.allcount += 1
        alldb.coal += 1
        ogdb.ogint1 += 80
        session2.commit()
        return

    elif num >= 958:
        ogdb.allcount += 1
        ogdb.breaking_pickaxe += 1
        alldb.allcount += 1
        alldb.breaking_pickaxe += 1
        ogdb.ogint1 -= 100
        session2.commit()
        return

    elif num >= 6:
        ogdb.allcount += 1
        ogdb.broken_pickaxe += 1
        alldb.allcount += 1
        alldb.broken_pickaxe += 1
        ogdb.ogint1 -= 400
        session2.commit()
        return

    else:
        ogdb.allcount += 1
        ogdb.death += 1
        alldb.allcount += 1
        alldb.death += 1
        ogdb.ogint1 -= 1111
        session2.commit()
        return


async def coregacha9(interaction: Interaction):
    num = random.randint(1, 100000)
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()

    if num >= 99915:
        og1_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ビーコン\n-# ** **\nNo.{num:06}\n確率: 0.086%\n経験値: +30000 XP",
            color=0x87ff37
        )
        og1_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og1_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 30000}XP")
        file1 = discord.File("assets/ore_gacha/Beacon.png", filename="Beacon.png")
        og1_embed.set_thumbnail(url="attachment://Beacon.png")
        await interaction.response.send_message(embed=og1_embed, file=file1, silent=True)
        xpdb.level += 3
        xpdb.alladdexp += 30000
        session.commit()
        ogdb.allcount += 1
        ogdb.beacon += 1
        alldb.allcount += 1
        alldb.beacon += 1
        ogdb.ogint1 += 30000
        session2.commit()
        return

    elif num >= 99004:
        og2_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ネザライトブロック\n-# ** **\nNo.{num:06}\n確率: 0.911%\n経験値: +20000 XP",
            color=0x87ff37
        )
        og2_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og2_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 20000}XP")
        file2 = discord.File("assets/ore_gacha/Block_of_Netherite.png", filename="Block_of_Netherite.png")
        og2_embed.set_thumbnail(url="attachment://Block_of_Netherite.png")
        await interaction.response.send_message(embed=og2_embed, file=file2, silent=True)
        xpdb.level += 2
        xpdb.alladdexp += 20000
        session.commit()
        ogdb.allcount += 1
        ogdb.netheriteb += 1
        alldb.allcount += 1
        alldb.netheriteb += 1
        ogdb.ogint1 += 20000
        session2.commit()
        return

    elif num >= 93118:
        og3_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ラピスラズリブロック\n-# ** **\nNo.{num:06}\n確率: 5.886%\n経験値: +1620 XP",
            color=0x87ff37
        )
        og3_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og3_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 1620}XP")
        file3 = discord.File("assets/ore_gacha/Block_of_Lapis_Lazuli.png", filename="Block_of_Lapis_Lazuli.png")
        og3_embed.set_thumbnail(url="attachment://Block_of_Lapis_Lazuli.png")
        await interaction.response.send_message(embed=og3_embed, file=file3, silent=True)
        xpdb.exp += 1620
        xpdb.alladdexp += 1620
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.lapisb += 1
        alldb.allcount += 1
        alldb.lapisb += 1
        ogdb.ogint1 += 1620
        session2.commit()
        return

    elif num >= 87223:
        og4_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ダイヤモンドブロック\n-# ** **\nNo.{num:06}\n確率: 5.895%\n経験値: +2250 XP",
            color=0x87ff37
        )
        og4_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og4_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 2250}XP")
        file4 = discord.File("assets/ore_gacha/Block_of_Diamond.png", filename="Block_of_Diamond.png")
        og4_embed.set_thumbnail(url="attachment://Block_of_Diamond.png")
        await interaction.response.send_message(embed=og4_embed, file=file4, silent=True)
        xpdb.exp += 2250
        xpdb.alladdexp += 2250
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.diamondb += 1
        alldb.allcount += 1
        alldb.diamondb += 1
        ogdb.ogint1 += 2250
        session2.commit()
        return

    elif num >= 81084:
        og5_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 金インゴットブロック\n-# ** **\nNo.{num:06}\n確率: 6.139%\n経験値: +1350 XP",
            color=0x87ff37
        )
        og5_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og5_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 1350}XP")
        file5 = discord.File("assets/ore_gacha/Block_of_Gold.png", filename="Block_of_Gold.png")
        og5_embed.set_thumbnail(url="attachment://Block_of_Gold.png")
        await interaction.response.send_message(embed=og5_embed, file=file5, silent=True)
        xpdb.exp += 1350
        xpdb.alladdexp += 1350
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.goldb += 1
        alldb.allcount += 1
        alldb.goldb += 1
        ogdb.ogint1 += 1350
        session2.commit()
        return

    elif num >= 73459:
        og6_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# レッドストーンブロック\n-# ** **\nNo.{num:06}\n確率: 7.625%\n経験値: +1170 XP",
            color=0x87ff37
        )
        og6_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og6_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 1170}XP")
        file6 = discord.File("assets/ore_gacha/Block_of_Redstone.png", filename="Block_of_Redstone.png")
        og6_embed.set_thumbnail(url="attachment://Block_of_Redstone.png")
        await interaction.response.send_message(embed=og6_embed, file=file6, silent=True)
        xpdb.exp += 1170
        xpdb.alladdexp += 1170
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.redstoneb += 1
        alldb.allcount += 1
        alldb.redstoneb += 1
        ogdb.ogint1 += 1170
        session2.commit()
        return

    elif num >= 62868:
        og7_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# エメラルドブロック\n-# ** **\nNo.{num:06}\n確率: 10.591%\n経験値: +900 XP",
            color=0x87ff37
        )
        og7_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og7_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 900}XP")
        file7 = discord.File("assets/ore_gacha/Block_of_Emerald.png", filename="Block_of_Emerald.png")
        og7_embed.set_thumbnail(url="attachment://Block_of_Emerald.png")
        await interaction.response.send_message(embed=og7_embed, file=file7, silent=True)
        xpdb.exp += 900
        xpdb.alladdexp += 900
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.emeraldb += 1
        alldb.allcount += 1
        alldb.emeraldb += 1
        ogdb.ogint1 += 900
        session2.commit()
        return

    elif num >= 51307:
        og8_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 鉄ブロック\n-# ** **\nNo.{num:06}\n確率: 11.561%\n経験値: +765 XP",
            color=0x87ff37
        )
        og8_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og8_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 765}XP")
        file8 = discord.File("assets/ore_gacha/Block_of_Iron.png", filename="Block_of_Iron.png")
        og8_embed.set_thumbnail(url="attachment://Block_of_Iron.png")
        await interaction.response.send_message(embed=og8_embed, file=file8, silent=True)
        xpdb.exp += 765
        xpdb.alladdexp += 765
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.ironb += 1
        alldb.allcount += 1
        alldb.ironb += 1
        ogdb.ogint1 += 765
        session2.commit()
        return

    elif num >= 35158:
        og9_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 銅ブロック\n-# ** **\nNo.{num:06}\n確率: 16.149%\n経験値: +360 XP",
            color=0x87ff37
        )
        og9_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og9_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 360}XP")
        file9 = discord.File("assets/ore_gacha/Block_of_Copper.png", filename="Block_of_Copper.png")
        og9_embed.set_thumbnail(url="attachment://Block_of_Copper.png")
        await interaction.response.send_message(embed=og9_embed, file=file9, silent=True)
        xpdb.exp += 360
        xpdb.alladdexp += 360
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.copperb += 1
        alldb.allcount += 1
        alldb.copperb += 1
        ogdb.ogint1 += 360
        session2.commit()
        return

    elif num >= 20597:
        og10_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ネザークオーツブロック\n-# ** **\nNo.{num:06}\n確率: 14.561%\n経験値: +220 XP",
            color=0x87ff37
        )
        og10_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og10_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 220}XP")
        file10 = discord.File("assets/ore_gacha/Block_of_Quartz.png", filename="Block_of_Quartz.png")
        og10_embed.set_thumbnail(url="attachment://Block_of_Quartz.png")
        await interaction.response.send_message(embed=og10_embed, file=file10, silent=True)
        xpdb.exp += 220
        xpdb.alladdexp += 220
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.quartzb += 1
        alldb.allcount += 1
        alldb.quartzb += 1
        ogdb.ogint1 += 220
        session2.commit()
        return

    elif num >= 8852:
        og11_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 石炭ブロック\n-# ** **\nNo.{num:06}\n確率: 11.745%\n経験値: +720 XP",
            color=0x87ff37
        )
        og11_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og11_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 + 720}XP")
        file11 = discord.File("assets/ore_gacha/Block_of_Coal.png", filename="Block_of_Coal.png")
        og11_embed.set_thumbnail(url="attachment://Block_of_Coal.png")
        await interaction.response.send_message(embed=og11_embed, file=file11, silent=True)
        xpdb.exp += 720
        xpdb.alladdexp += 720
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.coalb += 1
        alldb.allcount += 1
        alldb.coalb += 1
        ogdb.ogint1 += 720
        session2.commit()
        return

    elif num >= 958:
        og12_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 壊れたツルハシ\n-# ** **\nNo.{num:06}\n確率: 7.894%\n経験値: -1000 XP",
            color=0x87ff37
        )
        og12_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og12_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 - 1000}XP")
        file12 = discord.File("assets/ore_gacha/broken_pickaxe.png", filename="broken_pickaxe.png")
        og12_embed.set_thumbnail(url="attachment://broken_pickaxe.png")
        await interaction.response.send_message(embed=og12_embed, file=file12, silent=True)
        xpdb.exp -= 1000
        xpdb.allremoveexp += 1000
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.broken_pickaxe9 += 1
        alldb.allcount += 1
        alldb.broken_pickaxe9 += 1
        ogdb.ogint1 -= 1000
        session2.commit()
        return

    elif num >= 6:
        og13_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 死亡\n-# ** **\nNo.{num:06}\n確率: 0.952%\n経験値: -4000 XP",
            color=0x87ff37
        )
        og13_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og13_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 - 4000}XP")
        file13 = discord.File("assets/ore_gacha/death.png", filename="death.png")
        og13_embed.set_thumbnail(url="attachment://death.png")
        await interaction.response.send_message(embed=og13_embed, file=file13, silent=True)
        xpdb.exp -= 4000
        xpdb.allremoveexp += 4000
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.death9 += 1
        alldb.allcount += 1
        alldb.death9 += 1
        ogdb.ogint1 -= 4000
        session2.commit()
        return

    else:
        og14_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ワールドデータ破損\n-# ** **\nNo.{num:06}\n確率: 0.005%\n経験値: -10000 XP",
            color=0x87ff37
        )
        og14_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og14_embed.set_footer(text=f"本日残り: {10 - ogdb.dailygacha}回 / 今日の収支: {ogdb.ogint1 - 10000}XP")
        file14 = discord.File("assets/ore_gacha/missing_model.png", filename="missing_model.png")
        og14_embed.set_thumbnail(url="attachment://missing_model.png")
        await interaction.response.send_message(embed=og14_embed, file=file14, silent=True)
        xpdb.level -= 1
        xpdb.allremoveexp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.unkownworld += 1
        alldb.allcount += 1
        alldb.unkownworld += 1
        ogdb.ogint1 -= 10000
        session2.commit()
        return


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
            session2.add(Oregacha(userid=interaction.user.id, username=interaction.user.name))
            session2.commit()
            await interaction.response.send_message("ガチャデータベースにユーザーを登録しました\nもう一度実行してください(1日あたりの実行回数は減りません)\n次でガチャが回せるはずです", ephemeral=True)
            return
        if userdb.noxp is True:
            await interaction.response.send_message("あなたは経験値システムが無効化されてるからガチャ回せないよ!!", ephemeral=True)
            return
        if gachadb.dailygacha >= 10:
            await interaction.response.send_message(f"本日のガチャ回数が上限に達しました\nまた明日回してね(^^♪\n-# 00:00:00～00:01:00に更新されます\n本日の収支は{gachadb.ogint1}XPでした", ephemeral=True)
            return
        if datetime.day == 9 or datetime.day == 19 or datetime.day == 29:
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


async def setup(bot: commands.Bot):
    await bot.add_cog(COregacha(bot))
