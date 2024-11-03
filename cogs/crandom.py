from discord.ext import commands
import discord
from discord import app_commands
import random

anydot = ["...", "....", ".....", "......", ".......", "........"]


class CRandom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="crandom", description="ランダムな数字を出力します")
    @app_commands.describe(
        mode="value : 自分にのみ表示・roll : 全体に表示",
        range="送信したい内容を書いてください",
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="roll", value="mroll"),
            app_commands.Choice(name="value", value="mvalue"),
        ]
    )
    async def cybase64(
        self,
        interaction: discord.Interaction,
        mode: app_commands.Choice[str],
        range: str,
    ):
        if anydot in range:
            await interaction.response.send_message(
                "rangeで使うドットの数は2個です\n(例 : ..-10(-10以下)・10..(10以上))・1..30(1以上30以下)"
            )
        # スライスを用いて特定の文字より後ろを抽出
        s = "2021/03/23 05:30"

        target = ".."
        idx = s.find(target)
        r = s[idx + 1 :]  # スライスで半角空白文字のインデックス＋1以降を抽出

        print(r)  # 05:30
        text = range
        str1 = ".."
        aaa = (
            text[c + 1 :]
            if (c := text.find(str1)) != -1 and text.startswith(str1)
            else ""
        )
        bbb = text[:c] if (c := text.rfind(str1)) != -1 and text.endswith(str1) else ""
        ccc = text[:c] if (c := text.rfind(str1)) != -1 else ""
        ddd = text[c + len(str1) :] if (c := text.find(str1)) != -1 else ""

        if range.content.startswith("aaa"):
            number = random.randint(-2147483647, 2147483648)
            startnum = 1
            stopnum = 10

        if mode.value == "mroll":
            await interaction.response.send_message(
                f"{interaction.user.display_name}は{number}を引きました ( 値の範囲は{startnum}から{stopnum} )",
                ephemeral=False,
            )
        if mode.value == "mvalue":
            await interaction.response.send_message(f"乱数 : {number}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CRandom(bot))
