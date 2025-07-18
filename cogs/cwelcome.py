from discord.ext import commands
import discord
from config.config import config


class CWelcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # メンバーの状態変化を検知するイベント
    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        added_roles_id = [role.id for role in set(after.roles) - set(before.roles)]  # 増えたロールのid一覧
        if config.roles.regularmember in added_roles_id:

            channel = await self.bot.fetch_channel(config.freechat)  # 総合雑談チャンネルを取得
            await channel.send(f"{after.mention}さんが入所しました。コマ研へようこそ！\n<#{config.role_set_ch}>で自分にあったロールを設定してください。", silent=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CWelcome(bot))
