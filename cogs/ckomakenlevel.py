import math
import random
import re
from datetime import datetime

import discord
from discord.ext import commands, tasks

from config.config import config
from database import Oregacha, User, session, session2


@tasks.loop(seconds=60)
async def loop():
    now = datetime.now()
    results = session.query(User).all()
    results2 = session2.query(Oregacha).all()
    if now.hour == 0 and now.minute == 0:
        for i in results:
            i.dailylogin = False
            i.dailygivexp = False
        session.commit()
        for i2 in results2:
            i2.dailygacha = 0
            i2.ogint1 = 0
            i2.ogstr1 = ""
        session2.commit()
        print("リセット完了")


loop.start()


class Cmdbotlevel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        userdb = session.query(User).filter_by(userid=message.author.id).first()

        if not userdb and not message.author.bot:
            userdb = User(userid=message.author.id, username=message.author.name)
            session.add(userdb)
            session.commit()
            return

        if message.author.bot:
            return

        emoji_ptn = r"<a?:\w+:\d+>"
        unicode_emoji_ptn = r"[\U0001F900-\U0001FFFF]"
        mention_ptn = r"<@\d+>"
        combined_ptn = re.compile(f"(?:{emoji_ptn}|{unicode_emoji_ptn}|{mention_ptn})")

        if userdb.noxp is True and userdb:
            return
        elif message.content.startswith("ぬるぽ"):
            return
        elif message.content.startswith("NullPointerException"):
            return
        elif message.content.startswith("!d bump"):
            return
        elif message.content.startswith("/bump"):
            return
        elif message.content.startswith("oruvanoruvan"):
            return
        elif message.content.startswith("https://tenor.com/view/"):
            return
        elif len(combined_ptn.sub("", message.content).strip()) <= 5:
            return
        elif re.match(r"^(.+)\1+$", message.content):
            return

        if message.channel.id == config.listench:
            return
        elif message.channel.id == config.voicech:
            return
        elif message.channel.id == config.voice256ch:
            return
        elif message.channel.category_id == config.admin_category_id:
            start = 50 - math.floor(userdb.level / 10)
            end = 100 + math.floor(userdb.level / 10)
        elif message.channel.id == config.question_channels:
            start = 100 - math.floor(userdb.level / 10)
            end = 150 + math.floor(userdb.level / 10)
        else:
            start = 75 - math.floor(userdb.level / 10)
            end = 125 + math.floor(userdb.level / 10)
        if start < 0:
            start = 0
        exp_per_message = random.randint(start, end)
        userdb.chatcount += 1
        userdb.alladdexp += exp_per_message
        userdb.exp += exp_per_message
        session.commit()

        if message.channel.id == config.selfintroductionch:  # 書き換えること
            if userdb.selfintro is False:
                userdb.selfintro = True
                userdb.alladdexp += 200
                userdb.exp += 200
        elif message.channel.id == config.freechat:  # 書き換えること
            if userdb.freechat is False:
                userdb.freechat = True
                userdb.alladdexp += 200
                userdb.exp += 200
        elif message.channel.id == config.anotherch:  # 書き換えること
            if userdb.anotherch is False:
                userdb.anotherch = True
                userdb.alladdexp += 200
                userdb.exp += 200
        elif message.channel.id == config.question_channels:
            if userdb.question is False:
                userdb.question = True
                userdb.alladdexp += 200
                userdb.exp += 200
        session.commit()

        server_booster = message.guild.get_role(config.roles.serverbooster)
        if server_booster in message.author.roles:
            userdb.exp += 10
            userdb.alladdexp += 10
        session.commit()

        if userdb.dailylogin is False:
            userdb.dailylogin = True
            userdb.dailylogincount += 1
            if userdb.dailylogincount % 10 == 0:
                userdb.alladdexp += 300
                userdb.exp += 300
            else:
                userdb.alladdexp += 100
                userdb.exp += 100
        session.commit()

        if userdb.exp >= 10000:
            userdb.level += 1
            userdb.exp -= 10000
            session.commit()
            mee6_channel = await self.bot.fetch_channel(config.mee6.botch)
            await mee6_channel.send(
                f"mcmdlevel,{message.author.id},{message.author.name},{userdb.level}"
            )

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message: discord.Message):
        deluserdb = session.query(User).filter_by(userid=message.author.id).first()

        exp_per_delmsg = random.randint(75, 100)
        if message.author.bot:
            return

        emoji_ptn = r"<a?:\w+:\d+>"
        unicode_emoji_ptn = r"[\U0001F900-\U0001FFFF]"
        mention_ptn = r"<@\d+>"
        combined_ptn = re.compile(f"(?:{emoji_ptn}|{unicode_emoji_ptn}|{mention_ptn})")

        if message.content.startswith("ぬるぽ"):
            return
        elif message.content.startswith("NullPointerException"):
            return
        elif message.content.startswith("!d bump"):
            return
        elif message.content.startswith("/bump"):
            return
        elif message.content.startswith("oruvanoruvan"):
            return
        elif message.content.startswith("https://tenor.com/view/"):
            return
        elif len(combined_ptn.sub("", message.content).strip()) <= 5:
            return
        elif re.match(r"^(.+)\1+$", message.content):
            return

        if message.channel.id == config.listench:
            return
        elif message.channel.category_id == config.admin_category_id:
            return

        deluserdb.chatcount -= 1
        deluserdb.allremoveexp += exp_per_delmsg
        deluserdb.exp -= exp_per_delmsg

        server_booster = message.guild.get_role(config.roles.serverbooster)
        if server_booster in message.author.roles:
            deluserdb.exp -= 10
            deluserdb.allremoveexp += 10
        session.commit()

        if deluserdb.exp < 0:
            deluserdb.level -= 1
            deluserdb.exp += 10000
        session.commit()


async def setup(bot: commands.Bot):
    await bot.add_cog(Cmdbotlevel(bot))
