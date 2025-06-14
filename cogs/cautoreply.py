from discord.ext import commands
import discord
from config.config import config
import random
from datetime import datetime
import re

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


# ダイスロール判定関数
def parse_and_evaluate(expression: str):
    expression = expression.replace(" ", "")

    def evaluate_dice_expression(expr: str):
        tokens = expr.split('+')
        total = 0
        breakdown = []

        for token in tokens:
            token = token.strip().lower()
            if 'd' in token:
                num, sides = token.split('d')
                num = int(num) if num else 1
                sides = int(sides)
                rolls = [random.randint(1, sides) for _ in range(num)]
                total += sum(rolls)
                breakdown.append(f"{rolls}")
            else:
                val = int(token)
                total += val
                breakdown.append(str(val))

        return total, breakdown

    # 不等式を検出
    match = re.match(r'(.+?)(<=|>=|==|!=|<|>)(.+)', expression)
    if match:
        dice_expr, operator, target = match.groups()
        target = int(target)
        total, breakdown = evaluate_dice_expression(dice_expr)
        comparison_result = eval(f"{total} {operator} {target}")
        return {
            'type': 'comparison',
            'success': comparison_result,
            'result': total,
            'breakdown': breakdown,
            'operator': operator,
            'target': target
        }
    else:
        # 不等式がない → 単なるダイスロール
        total, breakdown = evaluate_dice_expression(expression)
        return {
            'type': 'roll',
            'result': total,
            'breakdown': breakdown
        }


class CAutoreply(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.channel.id == config.botcommand_channel_id:
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

            elif message.content.startswith("NullPointerException"):
                num = random.random()
                if num < 0.95:
                    await message.channel.send("ｶﾞｯ", silent=True)
                elif num < 0.98:
                    await message.channel.send("ｶﾞﾌﾞｯ", silent=True)
                else:
                    await message.channel.send(GABU, silent=True)
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

            elif message.content.startswith("/bump"):
                await message.channel.send(
                    embed=discord.Embed(
                        title="BUMPを実行出来てないよ!!",
                        color=0x00BFFF,
                        timestamp=datetime.now(),
                    ), silent=True
                )

            elif message.content.startswith("oruvanoruvan"):
                await message.channel.send(ORUVANORUVAN, silent=True)

            try:
                result = parse_and_evaluate(message.content)
            except ValueError:
                pass  # ダイスロールでなかった
            result["breakdown"] = map(lambda x: x.replace(" ", ""), result["breakdown"])
            embed = discord.Embed()
            if result["type"] == "roll":  # 成否判定なし
                embed.color = 0x808080
                embed.description = f"{"+".join(result["breakdown"])} = {result["result"]}"
            if result["type"] == "comparison":  # 成否判定あり
                embed.color = 0x456cba if result["success"] else 0xba4545
                embed.description = f"{"+".join(result["breakdown"])} = {result["result"]} {result["operator"]} {result["target"]} : {"成功" if result["success"] else "失敗"}"
            await message.reply(embed=embed, silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CAutoreply(bot))
