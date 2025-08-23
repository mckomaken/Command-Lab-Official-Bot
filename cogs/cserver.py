import datetime
import os
import sqlite3

import discord
import requests
from discord import app_commands
from discord.ext import commands

root = os.path.dirname(os.path.dirname(__file__))
db_name = os.path.join(root, "server.db")


# サーバー情報表示embed
def server_embed(ip: str, is_java: bool):
    url = f"https://api.mcstatus.io/v2/status/{'java' if is_java else 'bedrock'}/{ip}"
    response = requests.get(url)
    data = response.json()

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), "JST"))
    embed = discord.Embed(
        title=f"{ip}", description=f"取得日時：{now.strftime('%Y/%m/%d %H:%M:%S')}"
    )

    view = discord.ui.View()

    # オフラインの場合
    if data["online"] is False:
        embed.color = discord.Colour.red()
        embed.add_field(
            inline=False,
            name=f":x:オフライン",
            value="サーバーが起動していないか、アドレスが間違っています",
        )

    # オンラインの場合
    else:
        embed.color = discord.Colour.blue()
        embed.add_field(
            inline=False,
            name=f":white_check_mark:オンライン",
            value=f"```{data['motd']['clean']}```",
        )
        embed.add_field(
            inline=False,
            name=f"バージョン",
            value=f"{data['version']['name_clean']}",
        )
        embed.add_field(
            inline=False,
            name=f"プレイヤー",
            value=f"{data['players']['online']}人\n{', '.join(data['players']['list'])}",
        )
        # embed.set_thumbnail(f"https://api.mcstatus.io/v2/icon/{ip}")

    # お気に入り登録ボタン
    class LikeButton(discord.ui.Button):
        def __init__(self, ip, emoji, label, style, edition):
            super().__init__(emoji=emoji, label=label, style=style)
            self.ip = ip
            self.edition = edition

        async def callback(self, interaction: discord.Interaction):
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()

            cur.execute(f"select ips from server where userid = {interaction.user.id}")
            raw = cur.fetchall()

            # まだデータベースにユーザーidがなかった場合
            if not raw:
                cur.execute(
                    f'insert into server values({interaction.user.id}, "dict()")'
                )
                cur.execute(
                    f"select ips from server where userid = {interaction.user.id}"
                )
                raw = cur.fetchall()

            servers = eval(raw[0][0])

            # 既にお気に入り登録されていた場合
            if self.ip in servers.keys():
                await interaction.response.send_message(
                    f"`{self.ip}`は既にお気に入り登録されています", ephemeral=True
                )
                return

            # お気に入り件数が10件に達していた場合
            if len(servers) >= 10:
                await interaction.response.send_message(
                    f"お気に入り件数が上限の10に達しています", ephemeral=True
                )
                return

            servers[self.ip] = self.edition

            cur.execute(
                f'update server set ips = "{servers}" where userid = {interaction.user.id}'
            )
            conn.commit()

            cur.close()
            conn.close()

            await interaction.response.send_message(
                f"`{self.ip}`をお気に入りに追加しました", ephemeral=True
            )

    like = LikeButton(
        emoji="⭐",
        label="お気に入り登録",
        style=discord.ButtonStyle.secondary,
        ip=ip,
        edition="java" if is_java else "bedrock",
    )
    view.add_item(like)

    return embed, view


class CServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # cserverコマンドグループ
    cserver = app_commands.Group(name="cserver", description="サーバー表示")

    ######## サーバー状態表示コマンドJAVA(/server java)
    @cserver.command(name="java", description="Javaのサーバー情報を表示します")
    @app_commands.describe(ip="サーバーアドレス")
    async def java(self, interaction: discord.Interaction, ip: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed, view = server_embed(ip, True)
        await interaction.followup.send(embed=embed, view=view)

    # エラーハンドラ
    @java.error
    async def raise_error(self, ctx, error):
        print(error)

    ######## サーバー状態表示コマンドBEDROCK(/server bedrock)
    @cserver.command(name="bedrock", description="Bedrockのサーバー情報を表示します")
    @app_commands.describe(ip="サーバーアドレス")
    async def bedrock(self, interaction: discord.Interaction, ip: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed, view = server_embed(ip, False)
        await interaction.followup.send(embed=embed, view=view)

    # エラーハンドラ
    @bedrock.error
    async def raise_error(self, ctx, error):
        print(error)

    ######## お気に入りリスト表示(/server list)
    @cserver.command(name="list", description="お気に入りを表示します")
    async def clist(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cur.execute(f"select ips from server where userid = {interaction.user.id}")
        raw = cur.fetchall()

        cur.close()
        conn.close()

        # まだデータベースにユーザーidがなかった場合
        if not raw:
            await interaction.followup.send(
                f"お気に入り登録されているサーバーはありません", ephemeral=True
            )
            return

        servers = eval(raw[0][0])

        # お気に入りが空だった場合
        if servers == {}:
            await interaction.followup.send(
                f"お気に入り登録されているサーバーはありません", ephemeral=True
            )
            return

        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9), "JST")
        )
        embed = discord.Embed(
            title="お気に入りリスト",
            description=f"取得日時：{now.strftime('%Y/%m/%d %H:%M:%S')}",
            color=discord.Colour.blue(),
        )

        for ip, edition in servers.items():
            url = f"https://api.mcstatus.io/v2/status/{edition}/{ip}"
            response = requests.get(url)
            data = response.json()

            # オフラインの場合
            if data["online"] is False:
                embed.add_field(inline=False, name=f"{ip}", value=f":x:オフライン")

            # オンラインの場合
            embed.add_field(
                inline=False,
                name=f"{ip}",
                value=f":white_check_mark:オンライン　{data['players']['online']}人",
            )

        view = discord.ui.View()

        # お気に入り解除ボタン
        class RemoveButton(discord.ui.Button):
            def __init__(self, emoji, label, style, serverlist):
                super().__init__(emoji=emoji, label=label, style=style)
                self.serverlist = serverlist

            async def callback(self, interaction: discord.Interaction):
                view = discord.ui.View()

                # お気に入り解除サーバーの選択メニュー
                class RemoveSelect(discord.ui.Select):
                    async def callback(self, interaction: discord.Interaction):
                        target = interaction.data["values"][0]

                        conn = sqlite3.connect(db_name)
                        cur = conn.cursor()

                        cur.execute(
                            f"select ips from server where userid = {interaction.user.id}"
                        )
                        raw = cur.fetchall()
                        servers = eval(raw[0][0])
                        del servers[target]

                        cur.execute(
                            f'update server set ips = "{servers}" where userid = {interaction.user.id}'
                        )
                        conn.commit()

                        cur.close()
                        conn.close()

                        await interaction.response.send_message(
                            f"`{target}`をお気に入りから解除しました", ephemeral=True
                        )

                select = RemoveSelect(
                    placeholder="解除するサーバーを選択",
                    min_values=1,
                    max_values=1,
                    options=[
                        discord.SelectOption(label=server) for server in self.serverlist
                    ],
                )
                view.add_item(select)
                await interaction.response.send_message(view=view, ephemeral=True)

        like = RemoveButton(
            emoji="🗑",
            label="お気に入り解除",
            style=discord.ButtonStyle.secondary,
            serverlist=list(servers.keys()),
        )
        view.add_item(like)

        await interaction.followup.send(embed=embed, view=view)

    # エラーハンドラ
    @clist.error
    async def raise_error(self, ctx, error):
        print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(CServer(bot))
