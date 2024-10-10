from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from config.config import config
from utils.paginator import EmbedPaginator
from utils.util import create_codeblock


class CHelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chelp", description="このBotができること一覧")
    @app_commands.guild_only()
    async def chelp(self, interaction: discord.Interaction):
        embeds: list[discord.Embed] = []
        cmds: list[app_commands.Command] = []
        roles = [r.id for r in interaction.user.roles]

        for cmd in self.bot.tree.walk_commands():
            if cmd.description in "運営":
                if config.administrater_role_id not in roles:
                    continue
            if not isinstance(cmd, app_commands.Group):
                cmds.append(cmd)

        for i in range(0, len(cmds), 5):
            emb = discord.Embed(
                title="ヘルプ", timestamp=datetime.now(), color=0x00AA00
            )
            for command in cmds[i : i + 5]:
                c_name = "/" + command.qualified_name
                c_desc = create_codeblock(command.description)

                emb.add_field(name=f"{c_name}", value=c_desc, inline=False)

            embeds.append(emb)

        await EmbedPaginator(timeout=None).start(interaction, embeds)

    @app_commands.command(name="cping", description="pingを計測します")
    @app_commands.guild_only()
    @app_commands.describe(
        count="【初期値(未記入) : 1】実行回数を10以下の自然数で入力してください。",
        t_or_f="【初期値(未記入) : True】True : 3分おきに実行 ・ False : 直ぐ(１秒おき)に実行",
    )
    async def cping(
        self,
        interaction: discord.Interaction,
        count: Optional[int] = 1,
        t_or_f: Optional[bool] = True,
    ):
        latency_ms = round(self.bot.latency * 1000)
        latency_tick = round(self.bot.latency * 20)
        pi1JST_time = datetime.now()
        text1 = f"{latency_tick}tick\n{latency_ms}ms"

        ping1_embed = discord.Embed(
            title="現在のping", description=text1, color=0x400080, timestamp=pi1JST_time
        )

        if count > 10:
            await interaction.response.send_message(
                "countには10以下の自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪",
                ephemeral=True,
            )

        elif count >= 1 and count <= 10:
            await interaction.response.send_message(embed=ping1_embed)

            if count > 1:
                if t_or_f:  # true

                    @tasks.loop(minutes=3, count=count)  # ←あとで３分に変える
                    async def interval_cb():
                        pi2JST_time = datetime.now()
                        text2 = f"{latency_tick}tick\n{latency_ms}ms"

                        ping2_embed = discord.Embed(
                            title="現在のping",
                            description=text2,
                            color=0x400080,
                            timestamp=pi2JST_time,
                        )

                        await interaction.user.send(embed=ping2_embed)

                    interval_cb.start()

                elif t_or_f is False:  # false

                    @tasks.loop(seconds=1, count=count)
                    async def interval_cb():
                        pi3JST_time = datetime.now()
                        text3 = f"{latency_tick}tick\n{latency_ms}ms"

                        ping3_embed = discord.Embed(
                            title="現在のping",
                            description=text3,
                            color=0x400080,
                            timestamp=pi3JST_time,
                        )
                        await interaction.user.send(embed=ping3_embed)

                    interval_cb.start()

        else:
            await interaction.response.send_message(
                "countには10以下の自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(CHelpCog(bot))
