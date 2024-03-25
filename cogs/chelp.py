
from typing import Optional
import discord

from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks

HELP_MESSAGE = """
/chelp : この説明文が出てきます
/cping : サーバーとBotとのping値を測定できます
/cuuid : 2個のUUIDを自動生成してくれます
/cpack-mcmeta : ResourcePackとDataPackのpack_formatの番号一覧を表示します"
"""


class CHelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chelp", description="このBotができること一覧")
    @app_commands.guild_only()
    async def chelp(self, interaction: discord.Interaction):

        chJST_time = datetime.now()

        chelp_embed = discord.Embed(
            title="コマンド一覧",
            description=HELP_MESSAGE,
            color=0x2b9900,
            timestamp=chJST_time
        )

        await interaction.response.send_message(embed=chelp_embed)

    @app_commands.command(name="cping", description="pingを計測します")
    @app_commands.guild_only()
    @app_commands.describe(
        count="【初期値(未記入) : 1】実行回数を自然数で入力してください。",
        t_or_f="【初期値(未記入) : True】True : 3分おきに実行 ・ False : 直ぐ(１秒おき)に実行",
    )
    async def cping(self, interaction: discord.Interaction, count: Optional[int] = 1, t_or_f: Optional[bool] = True):

        pi1JST_time = datetime.now()
        text1 = f'{round(self.bot.latency*1000)}ms'

        ping1_embed = discord.Embed(
            title="現在のping",
            description=text1,
            color=0x400080,
            timestamp=pi1JST_time
        )

        if count >= 1:
            await interaction.response.send_message(embed=ping1_embed)

            if count > 1:
                if t_or_f:  # true
                    @tasks.loop(minutes=3, count=count)  # ←あとで３分に変える
                    async def interval_cb():

                        pi2JST_time = datetime.now()
                        text2 = f'{round(self.bot.latency*1000)}ms'

                        ping2_embed = discord.Embed(
                            title="現在のping",
                            description=text2,
                            color=0x400080,
                            timestamp=pi2JST_time
                        )

                        await interaction.user.send(embed=ping2_embed)

                    interval_cb.start()

                elif t_or_f is False:  # false
                    @tasks.loop(seconds=1, count=count)
                    async def interval_cb():

                        pi3JST_time = datetime.now()
                        text3 = f'{round(self.bot.latency*1000)}ms'

                        ping3_embed = discord.Embed(
                            title="現在のping",
                            description=text3,
                            color=0x400080,
                            timestamp=pi3JST_time
                        )
                        await interaction.user.send(embed=ping3_embed)

                    interval_cb.start()
        else:
            await interaction.response.send_message("countには自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CHelpCog(bot))
