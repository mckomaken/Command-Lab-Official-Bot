from discord.ext import commands
from datetime import datetime
from discord import app_commands, Interaction
import discord
from database import User, session, Oregacha, session2
import random


async def coregacha(interaction: Interaction):
    num = random.randint(1, 100000)
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()

    if num >= 99990:
        og1_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# ネザライトインゴット\n-# ** **\nNo.{num:06}\n確率: 0.011%\n経験値: +1720 XP",
            color=0xff9b37
        )
        og1_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og1_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file1 = discord.File("assets/ore_gacha/netherite_ingot.png", filename="netherite_ingot.png")
        og1_embed.set_thumbnail(url="attachment://netherite_ingot.png")
        await interaction.response.send_message(embed=og1_embed, file=file1, silent=True)
        xpdb.exp += 1720
        xpdb.alladdexp += 1720
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.netheritei += 1
        alldb.allcount += 1
        alldb.netheritei += 1
        session2.commit()
        return

    elif num >= 99935:
        og2_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# ネザライトの欠片\n-# ** **\nNo.{num:06}\n確率: 0.055%\n経験値: +300 XP",
            color=0xff9b37
        )
        og2_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og2_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file2 = discord.File("assets/ore_gacha/netherite_scrap.png", filename="netherite_scrap.png")
        og2_embed.set_thumbnail(url="attachment://netherite_scrap.png")
        await interaction.response.send_message(embed=og2_embed, file=file2, silent=True)
        xpdb.exp += 300
        xpdb.alladdexp += 300
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.netherites += 1
        alldb.allcount += 1
        alldb.netherites += 1
        session2.commit()
        return

    elif num >= 96049:
        og3_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# ラピスラズリ\n-# ** **\nNo.{num:06}\n確率: 3.886%\n経験値: +160 XP",
            color=0xff9b37
        )
        og3_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og3_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file3 = discord.File("assets/ore_gacha/lapis_lazuli.png", filename="lapis_lazuli.png")
        og3_embed.set_thumbnail(url="attachment://lapis_lazuli.png")
        await interaction.response.send_message(embed=og3_embed, file=file3, silent=True)
        xpdb.exp += 160
        xpdb.alladdexp += 160
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.lapis += 1
        alldb.allcount += 1
        alldb.lapis += 1
        session2.commit()
        return

    elif num >= 92154:
        og4_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# ダイヤモンド\n-# ** **\nNo.{num:06}\n確率: 3.895%\n経験値: +155 XP",
            color=0xff9b37
        )
        og4_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og4_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file4 = discord.File("assets/ore_gacha/diamond.png", filename="diamond.png")
        og4_embed.set_thumbnail(url="attachment://diamond.png")
        await interaction.response.send_message(embed=og4_embed, file=file4, silent=True)
        xpdb.exp += 155
        xpdb.alladdexp += 155
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.diamond += 1
        alldb.allcount += 1
        alldb.diamond += 1
        session2.commit()
        return

    elif num >= 88015:
        og5_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 金インゴット\n-# ** **\nNo.{num:06}\n確率: 4.139%\n経験値: +130 XP",
            color=0xff9b37
        )
        og5_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og5_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file5 = discord.File("assets/ore_gacha/gold_ingot.png", filename="gold_ingot.png")
        og5_embed.set_thumbnail(url="attachment://gold_ingot.png")
        await interaction.response.send_message(embed=og5_embed, file=file5, silent=True)
        xpdb.exp += 130
        xpdb.alladdexp += 130
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.gold += 1
        alldb.allcount += 1
        alldb.gold += 1
        session2.commit()
        return

    elif num >= 82390:
        og6_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# レッドストーン\n-# ** **\nNo.{num:06}\n確率: 5.625%\n経験値: +110 XP",
            color=0xff9b37
        )
        og6_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og6_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file6 = discord.File("assets/ore_gacha/redstone_dust.png", filename="redstone_dust.png")
        og6_embed.set_thumbnail(url="attachment://redstone_dust.png")
        await interaction.response.send_message(embed=og6_embed, file=file6, silent=True)
        xpdb.exp += 110
        xpdb.alladdexp += 110
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.redstone += 1
        alldb.allcount += 1
        alldb.redstone += 1
        session2.commit()
        return

    elif num >= 73268:
        og7_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# エメラルド\n-# ** **\nNo.{num:06}\n確率: 9.122%\n経験値: +90 XP",
            color=0xff9b37
        )
        og7_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og7_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file7 = discord.File("assets/ore_gacha/emerald.png", filename="emerald.png")
        og7_embed.set_thumbnail(url="attachment://emerald.png")
        await interaction.response.send_message(embed=og7_embed, file=file7, silent=True)
        xpdb.exp += 90
        xpdb.alladdexp += 90
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.emerald += 1
        alldb.allcount += 1
        alldb.emerald += 1
        session2.commit()
        return

    elif num >= 61707:
        og8_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 鉄インゴット\n-# ** **\nNo.{num:06}\n確率: 11.561%\n経験値: +75 XP",
            color=0xff9b37
        )
        og8_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og8_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file8 = discord.File("assets/ore_gacha/iron_ingot.png", filename="iron_ingot.png")
        og8_embed.set_thumbnail(url="attachment://iron_ingot.png")
        await interaction.response.send_message(embed=og8_embed, file=file8, silent=True)
        xpdb.exp += 75
        xpdb.alladdexp += 75
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.iron += 1
        alldb.allcount += 1
        alldb.iron += 1
        session2.commit()
        return

    elif num >= 37558:
        og9_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 銅インゴット\n-# ** **\nNo.{num:06}\n確率: 24.149%\n経験値: +30 XP",
            color=0xff9b37
        )
        og9_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og9_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file9 = discord.File("assets/ore_gacha/copper_ingot.png", filename="copper_ingot.png")
        og9_embed.set_thumbnail(url="attachment://copper_ingot.png")
        await interaction.response.send_message(embed=og9_embed, file=file9, silent=True)
        xpdb.exp += 30
        xpdb.alladdexp += 30
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.copper += 1
        alldb.allcount += 1
        alldb.copper += 1
        session2.commit()
        return

    elif num >= 22597:
        og10_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# ネザークオーツ\n-# ** **\nNo.{num:06}\n確率: 14.961%\n経験値: +50 XP",
            color=0xff9b37
        )
        og10_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og10_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file10 = discord.File("assets/ore_gacha/nether_quartz.png", filename="nether_quartz.png")
        og10_embed.set_thumbnail(url="attachment://nether_quartz.png")
        await interaction.response.send_message(embed=og10_embed, file=file10, silent=True)
        xpdb.exp += 50
        xpdb.alladdexp += 50
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.quartz += 1
        alldb.allcount += 1
        alldb.quartz += 1
        session2.commit()
        return

    elif num >= 10852:
        og11_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 石炭\n-# ** **\nNo.{num:06}\n確率: 11.745%\n経験値: +70 XP",
            color=0xff9b37
        )
        og11_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og11_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file11 = discord.File("assets/ore_gacha/coal.png", filename="coal.png")
        og11_embed.set_thumbnail(url="attachment://coal.png")
        await interaction.response.send_message(embed=og11_embed, file=file11, silent=True)
        xpdb.exp += 70
        xpdb.alladdexp += 70
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.coal += 1
        alldb.allcount += 1
        alldb.coal += 1
        session2.commit()
        return

    elif num >= 958:
        og12_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 壊れかけのツルハシ\n-# ** **\nNo.{num:06}\n確率: 9.894%\n経験値: -100 XP",
            color=0xff9b37
        )
        og12_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og12_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file12 = discord.File("assets/ore_gacha/breaking_pickaxe.png", filename="breaking_pickaxe.png")
        og12_embed.set_thumbnail(url="attachment://breaking_pickaxe.png")
        await interaction.response.send_message(embed=og12_embed, file=file12, silent=True)
        xpdb.exp -= 100
        xpdb.allremoveexp += 100
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.breaking_pickaxe += 1
        alldb.allcount += 1
        alldb.breaking_pickaxe += 1
        session2.commit()
        return

    elif num >= 6:
        og13_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 壊れたツルハシ\n-# ** **\nNo.{num:06}\n確率: 0.952%\n経験値: -400 XP",
            color=0xff9b37
        )
        og13_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og13_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file13 = discord.File("assets/ore_gacha/broken_pickaxe.png", filename="broken_pickaxe.png")
        og13_embed.set_thumbnail(url="attachment://broken_pickaxe.png")
        await interaction.response.send_message(embed=og13_embed, file=file13, silent=True)
        xpdb.exp -= 400
        xpdb.allremoveexp += 400
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.broken_pickaxe += 1
        alldb.allcount += 1
        alldb.broken_pickaxe += 1
        session2.commit()
        return

    else:
        og14_embed = discord.Embed(
            title="ガチャ結果",
            description=f"# 死亡\n-# ** **\nNo.{num:06}\n確率: 0.005%\n経験値: -1111 XP",
            color=0xff9b37
        )
        og14_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og14_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file14 = discord.File("assets/ore_gacha/death.png", filename="death.png")
        og14_embed.set_thumbnail(url="attachment://death.png")
        await interaction.response.send_message(embed=og14_embed, file=file14, silent=True)
        xpdb.exp -= 1111
        xpdb.allremoveexp += 1111
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.death += 1
        alldb.allcount += 1
        alldb.death += 1
        session2.commit()
        return


async def coregacha9(interaction: Interaction):
    num = random.randint(1, 100000)
    xpdb = session.query(User).filter_by(userid=interaction.user.id).first()
    ogdb = session2.query(Oregacha).filter_by(userid=interaction.user.id).first()
    alldb = session2.query(Oregacha).filter_by(userid="101").first()

    if num >= 99990:
        og1_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ビーコン\n-# ** **\nNo.{num:06}\n確率: 0.011%\n経験値: +20000 XP",
            color=0x87ff37
        )
        og1_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og1_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file1 = discord.File("assets/ore_gacha/Beacon.png", filename="Beacon.png")
        og1_embed.set_thumbnail(url="attachment://Beacon.png")
        await interaction.response.send_message(embed=og1_embed, file=file1, silent=True)
        xpdb.level += 2
        xpdb.alladdexp += 20000
        session.commit()
        ogdb.allcount += 1
        ogdb.beacon += 1
        alldb.allcount += 1
        alldb.beacon += 1
        session2.commit()
        return

    elif num >= 99935:
        og2_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ネザライトブロック\n-# ** **\nNo.{num:06}\n確率: 0.055%\n経験値: +10000 XP",
            color=0x87ff37
        )
        og2_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og2_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file2 = discord.File("assets/ore_gacha/Block_of_Netherite.png", filename="Block_of_Netherite.png")
        og2_embed.set_thumbnail(url="attachment://Block_of_Netherite.png")
        await interaction.response.send_message(embed=og2_embed, file=file2, silent=True)
        xpdb.level += 1
        xpdb.alladdexp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.netheriteb += 1
        alldb.allcount += 1
        alldb.netheriteb += 1
        session2.commit()
        return

    elif num >= 96049:
        og3_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ラピスラズリブロック\n-# ** **\nNo.{num:06}\n確率: 3.886%\n経験値: +1440 XP",
            color=0x87ff37
        )
        og3_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og3_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file3 = discord.File("assets/ore_gacha/Block_of_Lapis_Lazuli.png", filename="Block_of_Lapis_Lazuli.png")
        og3_embed.set_thumbnail(url="attachment://Block_of_Lapis_Lazuli.png")
        await interaction.response.send_message(embed=og3_embed, file=file3, silent=True)
        xpdb.exp += 1440
        xpdb.alladdexp += 1440
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.lapisb += 1
        alldb.allcount += 1
        alldb.lapisb += 1
        session2.commit()
        return

    elif num >= 92154:
        og4_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ダイヤモンドブロック\n-# ** **\nNo.{num:06}\n確率: 3.895%\n経験値: +1395 XP",
            color=0x87ff37
        )
        og4_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og4_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file4 = discord.File("assets/ore_gacha/Block_of_Diamond.png", filename="Block_of_Diamond.png")
        og4_embed.set_thumbnail(url="attachment://Block_of_Diamond.png")
        await interaction.response.send_message(embed=og4_embed, file=file4, silent=True)
        xpdb.exp += 1395
        xpdb.alladdexp += 1395
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.diamondb += 1
        alldb.allcount += 1
        alldb.diamondb += 1
        session2.commit()
        return

    elif num >= 88015:
        og5_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 金インゴットブロック\n-# ** **\nNo.{num:06}\n確率: 4.139%\n経験値: +1170 XP",
            color=0x87ff37
        )
        og5_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og5_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file5 = discord.File("assets/ore_gacha/Block_of_Gold.png", filename="Block_of_Gold.png")
        og5_embed.set_thumbnail(url="attachment://Block_of_Gold.png")
        await interaction.response.send_message(embed=og5_embed, file=file5, silent=True)
        xpdb.exp += 1170
        xpdb.alladdexp += 1170
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.goldb += 1
        alldb.allcount += 1
        alldb.goldb += 1
        session2.commit()
        return

    elif num >= 82390:
        og6_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# レッドストーンブロック\n-# ** **\nNo.{num:06}\n確率: 5.625%\n経験値: +990 XP",
            color=0x87ff37
        )
        og6_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og6_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file6 = discord.File("assets/ore_gacha/Block_of_Redstone.png", filename="Block_of_Redstone.png")
        og6_embed.set_thumbnail(url="attachment://Block_of_Redstone.png")
        await interaction.response.send_message(embed=og6_embed, file=file6, silent=True)
        xpdb.exp += 990
        xpdb.alladdexp += 990
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.redstoneb += 1
        alldb.allcount += 1
        alldb.redstoneb += 1
        session2.commit()
        return

    elif num >= 73268:
        og7_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# エメラルドブロック\n-# ** **\nNo.{num:06}\n確率: 9.122%\n経験値: +810 XP",
            color=0x87ff37
        )
        og7_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og7_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file7 = discord.File("assets/ore_gacha/Block_of_Emerald.png", filename="Block_of_Emerald.png")
        og7_embed.set_thumbnail(url="attachment://Block_of_Emerald.png")
        await interaction.response.send_message(embed=og7_embed, file=file7, silent=True)
        xpdb.exp += 810
        xpdb.alladdexp += 810
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.emeraldb += 1
        alldb.allcount += 1
        alldb.emeraldb += 1
        session2.commit()
        return

    elif num >= 61707:
        og8_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 鉄ブロック\n-# ** **\nNo.{num:06}\n確率: 11.561%\n経験値: +675 XP",
            color=0x87ff37
        )
        og8_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og8_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file8 = discord.File("assets/ore_gacha/Block_of_Iron.png", filename="Block_of_Iron.png")
        og8_embed.set_thumbnail(url="attachment://Block_of_Iron.png")
        await interaction.response.send_message(embed=og8_embed, file=file8, silent=True)
        xpdb.exp += 675
        xpdb.alladdexp += 675
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.ironb += 1
        alldb.allcount += 1
        alldb.ironb += 1
        session2.commit()
        return

    elif num >= 37558:
        og9_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 銅ブロック\n-# ** **\nNo.{num:06}\n確率: 24.149%\n経験値: +270 XP",
            color=0x87ff37
        )
        og9_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og9_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file9 = discord.File("assets/ore_gacha/Block_of_Copper.png", filename="Block_of_Copper.png")
        og9_embed.set_thumbnail(url="attachment://Block_of_Copper.png")
        await interaction.response.send_message(embed=og9_embed, file=file9, silent=True)
        xpdb.exp += 270
        xpdb.alladdexp += 270
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.copperb += 1
        alldb.allcount += 1
        alldb.copperb += 1
        session2.commit()
        return

    elif num >= 22597:
        og10_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ネザークオーツブロック\n-# ** **\nNo.{num:06}\n確率: 14.961%\n経験値: +200 XP",
            color=0x87ff37
        )
        og10_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og10_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file10 = discord.File("assets/ore_gacha/Block_of_Quartz.png", filename="Block_of_Quartz.png")
        og10_embed.set_thumbnail(url="attachment://Block_of_Quartz.png")
        await interaction.response.send_message(embed=og10_embed, file=file10, silent=True)
        xpdb.exp += 200
        xpdb.alladdexp += 200
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.quartzb += 1
        alldb.allcount += 1
        alldb.quartzb += 1
        session2.commit()
        return

    elif num >= 10852:
        og11_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 石炭ブロック\n-# ** **\nNo.{num:06}\n確率: 11.745%\n経験値: +630 XP",
            color=0x87ff37
        )
        og11_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og11_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file11 = discord.File("assets/ore_gacha/Block_of_Coal.png", filename="Block_of_Coal.png")
        og11_embed.set_thumbnail(url="attachment://Block_of_Coal.png")
        await interaction.response.send_message(embed=og11_embed, file=file11, silent=True)
        xpdb.exp += 630
        xpdb.alladdexp += 630
        if xpdb.exp >= 10000:
            xpdb.level += 1
            xpdb.exp -= 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.coalb += 1
        alldb.allcount += 1
        alldb.coalb += 1
        session2.commit()
        return

    elif num >= 958:
        og12_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 壊れたツルハシ\n-# ** **\nNo.{num:06}\n確率: 9.894%\n経験値: -900 XP",
            color=0x87ff37
        )
        og12_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og12_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file12 = discord.File("assets/ore_gacha/broken_pickaxe.png", filename="broken_pickaxe.png")
        og12_embed.set_thumbnail(url="attachment://broken_pickaxe.png")
        await interaction.response.send_message(embed=og12_embed, file=file12, silent=True)
        xpdb.exp -= 900
        xpdb.allremoveexp += 900
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.broken_pickaxe9 += 1
        alldb.allcount += 1
        alldb.broken_pickaxe9 += 1
        session2.commit()
        return

    elif num >= 6:
        og13_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# 死亡\n-# ** **\nNo.{num:06}\n確率: 0.952%\n経験値: -3600 XP",
            color=0x87ff37
        )
        og13_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og13_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
        file13 = discord.File("assets/ore_gacha/death.png", filename="death.png")
        og13_embed.set_thumbnail(url="attachment://death.png")
        await interaction.response.send_message(embed=og13_embed, file=file13, silent=True)
        xpdb.exp -= 3600
        xpdb.allremoveexp += 3600
        if xpdb.exp < 0:
            xpdb.level -= 1
            xpdb.exp += 10000
        session.commit()
        ogdb.allcount += 1
        ogdb.death9 += 1
        alldb.allcount += 1
        alldb.death9 += 1
        session2.commit()
        return

    else:
        og14_embed = discord.Embed(
            title="【約9倍デー】ガチャ結果",
            description=f"# ワールドデータ破損\n-# ** **\nNo.{num:06}\n確率: 0.005%\n経験値: -10000 XP",
            color=0x87ff37
        )
        og14_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        og14_embed.set_footer(text=f"本日残り回数: {10 - ogdb.dailygacha}回")
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
            await interaction.response.send_message("本日のガチャ回数が上限に達しました\nまた明日回してね(^^♪\n-# 00:00:00～00:01:00に更新されます", ephemeral=True)
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
