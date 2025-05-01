from discord.ext import commands
from discord import Member, app_commands, Color
import discord
import math


# エラー定義
class CalculateError(Exception):
    def __init__(self, description):
        self.args = (description,)


# 定数
const = {
    "e": math.e,
    "pi": math.pi,
    "個": 1,
    "st": 64,
    "lc": 64 * 54,
    "deg": math.pi / 180,
}

# 1変数関数
func1 = {
    "sqrt": math.sqrt,
    "ln": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "arcsin": math.asin,
    "arccos": math.acos,
    "arctan": math.atan,
    "exp": math.exp,
}
# 2変数関数
func2 = {
    "log": lambda a, b: math.log(b, a),
}

# 二項演算子（乗法除法系）
kakewari = {
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "%": lambda x, y: x % y,
}

# 二項演算子（加法減法系）
tashihiki = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
}


keywords = (
    list(const.keys())
    + list(func1.keys())
    + list(func2.keys())
    + list(kakewari.keys())
    + list(tashihiki.keys())
    + ["^", "(", ")", "->"]
)
keywords.sort(reverse=True, key=len)


# 計算
def calculate(text):

    # 式を要素ごとに分割
    def divide(text):
        separate = set()
        for keyword in keywords:
            start = 0
            end = 0
            no_keywords_left = False
            while True:
                while not keyword in text[start:end]:
                    if end == len(text):  # もうないから次のkeywordいこう
                        no_keywords_left = True
                        break
                    end += 1
                if no_keywords_left:
                    break
                while keyword in text[start:end]:
                    if keyword == text[start:end]:  # startを繰り上げよう
                        stop_separate = False
                        for i in range(
                            len(separate) - 1
                        ):  # separateする前に、今separateしようとしたところが既にseparateされた文字列の一部でないか確認する
                            if (
                                sorted(separate)[i] <= start
                                and end <= sorted(separate)[i + 1]
                                and text[sorted(separate)[i] : sorted(separate)[i + 1]]
                                in keywords
                            ):
                                stop_separate = True
                                break
                        if not stop_separate:
                            separate |= {start, end}
                        break
                    start += 1
                start = end

        separate -= {0, len(text)}
        separate = sorted(list(separate), reverse=True)
        result = [text]
        for s in separate:
            former = result.pop(0)
            result = [former[:s], former[s:]] + result

        return result

    elelist = divide(text)

    def cal_core(eles):
        # ()があれば再帰で処理させる
        i = 0
        while i < len(eles):
            if eles[i] == "(":
                start = i
                while eles[i] != ")":
                    i += 1
                    if i == len(eles):
                        raise CalculateError("カッコが閉じられていません！")
                end = i
                result = cal_core(eles[start + 1 : end])
                for _ in range(end - start + 1):
                    eles.pop(start)
                eles.insert(start, result)
                i = start
            i += 1

        for i in range(len(eles)):
            # floatに変換できるものはしておく
            try:
                eles[i] = float(eles[i])
            except:
                pass

            # 定数を数へ変換
            if eles[i] in const.keys():
                eles[i] = const[eles[i]]

        # 関数を処理
        i = -1
        while i < len(eles) - 1:
            i += 1
            if eles[i] in func1.keys():
                try:
                    x = eles.pop(i + 1)
                except:
                    raise CalculateError(f"{eles[i]}の引数指定が無効です！")
                eles[i] = func1[eles[i]](x)
            if eles[i] in func2.keys():
                try:
                    x = eles.pop(i + 1)
                    y = eles.pop(i + 1)
                except:
                    raise CalculateError(f"{eles[i]}の引数指定が無効です！")
                eles[i] = func2[eles[i]](x, y)

        # 累乗を処理（右から計算）
        i = len(eles)
        while i > 0:
            i -= 1
            if eles[i] == "^":
                try:
                    y = eles.pop(i + 1)
                    x = eles.pop(i - 1)
                except:
                    raise CalculateError(f"累乗の形式が無効です！")
                i -= 1
                eles[i] = x**y

        # 二項演算子を処理（左から計算）する関数
        def bin_op(dic):
            i = -1
            while i < len(eles) - 1:
                i += 1
                if eles[i] in dic.keys():
                    try:
                        y = eles.pop(i + 1)
                        x = eles.pop(i - 1)
                    except:
                        raise CalculateError(f"{eles[i-1]}の引数指定が無効です！")
                    i -= 1
                    eles[i] = dic[eles[i]](x, y)

        bin_op({"->": lambda x, y: x / y})  # 単位変換

        # 隣接している数は掛ける（左から計算）
        i = -1
        while i < len(eles) - 1:
            i += 1
            if isinstance(eles[i], float) and i < len(eles) - 1:
                if isinstance(eles[i + 1], float):
                    x = eles.pop(i + 1)
                    eles[i] *= x

        try:
            bin_op(kakewari)  # 乗法除法系
        except ZeroDivisionError:
            raise CalculateError(f"ゼロ除算が発生しました！")
        bin_op(tashihiki)  # 加法減法系

        if len(eles) != 1:
            raise CalculateError(f"エラーが発生しました！")

        return eles[0]

    result = round(cal_core(elelist), 12)  # 小数点以下12桁で丸める
    if result == int(result):  # 整数なら整数にする
        result = int(result)

    return result


view = discord.ui.View()
buttons = [
    discord.ui.Button(label="→", row=0, custom_id="cto"),
    discord.ui.Button(label="個", row=0, custom_id="citem"),
    discord.ui.Button(label="st", row=0, custom_id="cst"),
    discord.ui.Button(label="lc", row=0, custom_id="clc"),
    discord.ui.Button(label="(", row=0, custom_id="cstart"),
    discord.ui.Button(label="7", row=1, custom_id="c7"),
    discord.ui.Button(label="8", row=1, custom_id="c8"),
    discord.ui.Button(label="9", row=1, custom_id="c9"),
    discord.ui.Button(label="/", row=1, custom_id="cdiv"),
    discord.ui.Button(label=")", row=1, custom_id="cend"),
    discord.ui.Button(label="4", row=2, custom_id="c4"),
    discord.ui.Button(label="5", row=2, custom_id="c5"),
    discord.ui.Button(label="6", row=2, custom_id="c6"),
    discord.ui.Button(label="*", row=2, custom_id="cmul"),
    discord.ui.Button(label="^", row=2, custom_id="cbeki"),
    discord.ui.Button(label="1", row=3, custom_id="c1"),
    discord.ui.Button(label="2", row=3, custom_id="c2"),
    discord.ui.Button(label="3", row=3, custom_id="c3"),
    discord.ui.Button(label="-", row=3, custom_id="csub"),
    discord.ui.Button(label="del",row=3,custom_id="cdel"),
    discord.ui.Button(label="0", row=4, custom_id="c0"),
    discord.ui.Button(label=".", row=4, custom_id="cdot"),
    discord.ui.Button(label="=", row=4, custom_id="cequal", style=discord.ButtonStyle.primary),
    discord.ui.Button(label="+", row=4, custom_id="cadd"),
    discord.ui.Button(label="C", row=4, custom_id="cc"),
]
for button in buttons:
    view.add_item(button)


#本体
class CCalculate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ccalculate", description="計算します")
    @app_commands.describe(text="数式(空の場合電卓が表示されます)")
    async def ccalculate(self, interaction: discord.Interaction, text: str = ""):

        if text == "":
            embed = discord.Embed(color=Color.blue(), title="", description="```0```")
            await interaction.channel.send(embed=embed, view=view)

        else:
            try:
                await interaction.response.send_message(calculate(text), ephemeral=True)
            except CalculateError as e:
                embed = discord.Embed(
                    color=Color.red(),
                    title="エラー",
                    description=f"{e.args[0]}：`{text}`",
                )
                await interaction.response.send_message(embed=embed)

    # ボタンを押されたときの処理
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data["custom_id"]
        button_id = {
            "cto": "->",
            "citem": "個",
            "cst": "st",
            "clc": "lc",
            "c7": "7",
            "c8": "8",
            "c9": "9",
            "cdiv": "/",
            "cstart": "(",
            "c4": "4",
            "c5": "5",
            "c6": "6",
            "cmul": "*",
            "cend": ")",
            "c1": "1",
            "c2": "2",
            "c3": "3",
            "csub": "-",
            "c0": "0",
            "cdot": ".",
            "cadd": "+",
            "cbeki":"^"
        }
        embed = interaction.message.embeds[0]
        embed.title = ""
        text = embed.description.replace("```","")
        if custom_id in button_id.keys(): #文字入力キーの場合
            if text == "0":
                text = f"```{button_id[custom_id]}```"
            else:
                text = f"```{text}{button_id[custom_id]}```"
            embed.description = text

        elif custom_id == "cequal": #計算実行
            try:
                embed.description = f"```{calculate(text)}```"
            except CalculateError as e:
                embed.description = "```0```"
                embed.title = e.args[0]

        elif custom_id == "cc": #リセット
            embed.description = "```0```"

        elif custom_id == "cdel": #1文字消去
            text = f"```{text[:-1]}```"
            if text == "``````":
                text = "```0```"
            embed.description = text
        await interaction.response.edit_message(embed=embed,view=view)

    @ccalculate.error
    async def raise_error(self, ctx, error):
        print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(CCalculate(bot))
