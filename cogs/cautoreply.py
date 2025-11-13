import random
from datetime import datetime

import discord
from discord.ext import commands

from config.config import config

ORUVANORUVAN = """
ஒருவன் ஒருவன் முதலாளி
உலகில் மற்றவன் தொழிலாளி
விதியை நினைப்பவன் ஏமாளி
அதை வென்று முடிப்பவன் அறிவாளி

பூமியை வெல்ல ஆயுதம் எதற்கு
பூப்பறிக்க கோடரி எதற்கு
பொன்னோ பொருளோ போர்க்களம் எதற்கு
ஆசை துறந்தால் அகிலம் உனக்கு
"""


GABU = """
**　　**Λ＿Λ　　＼＼
　 （　・∀・）　　　|　|　ｶﾞｯ
　と　　　　）　 　 |　|
　　 Ｙ　/ノ　　　 人
　　　 /　）　 　 < 　>_Λ∩
　 ＿/し'　／／. Ｖ｀Д´）/
　（＿フ彡　　　　　 　　/　←>>1
"""


class AutoReplyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.channel.id == config.channels.bot_command_channel_id:
            if message.author.bot:
                return

            elif message.content.startswith("ぬるぽ"):
                num = random.random()
                if num < 0.9:
                    await message.channel.send("ｶﾞｯ", silent=True)
                elif num < 0.96:
                    await message.channel.send("ｶﾞﾌﾞｯ", silent=True)
                else:
                    await message.channel.send(GABU, silent=True)

                return

            elif message.content.startswith("NullPointerException"):
                num = random.random()
                if num < 0.95:
                    await message.channel.send("ｶﾞｯ", silent=True)
                elif num < 0.98:
                    await message.channel.send("ｶﾞﾌﾞｯ", silent=True)
                else:
                    await message.channel.send(GABU, silent=True)

                return
            # elif message.content.startswith("あけおめ"):
            #     num = random.random()
            #     if num < 0.6:
            #         await message.channel.send("ことよろ", silent=True)
            #     else:
            #         await message.channel.send("今年もよろしくお願いいたします！", silent=True)
            # elif message.content.startswith("あけましておめでとうございます"):
            #     num = random.random()
            #     if num < 0.4:
            #         await message.channel.send("ことよろ", silent=True)
            #     else:
            #         await message.channel.send("今年もよろしくお願いいたします！", silent=True)

            elif message.content.startswith("!d bump"):
                await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)", silent=True)
                return

            elif message.content.startswith("/bump"):
                await message.channel.send(
                    embed=discord.Embed(
                        title="BUMPを実行出来てないよ!!",
                        color=0x00BFFF,
                        timestamp=datetime.now(),
                    ),
                    silent=True,
                )
                return

            elif message.content.startswith("oruvanoruvan"):
                await message.channel.send(ORUVANORUVAN, silent=True)
                return


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoReplyCog(bot))
