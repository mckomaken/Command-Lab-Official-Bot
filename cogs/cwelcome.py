import discord
from discord.ext import commands

from config.config import config
from database import User, session


class CWelcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # メンバーの状態変化を検知するイベント
    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        added_roles_id = [role.id for role in set(after.roles) - set(before.roles)]  # 増えたロールのid一覧
        if config.roles.regularmember in added_roles_id:

            channel = await self.bot.fetch_channel(config.channels.invite)  # 入所者チャンネルを取得
            welcome_embed = discord.Embed(
                description=f"コマ研へようこそ！あなたは無事認証されました！\n<#{config.channels.role_set}>で自分にあったロールを設定しましょう(^O^)/",
                color=discord.Color.green()
            )
            await channel.send(f"{after.mention}さんが入所しました！", embed=welcome_embed, silent=True)
        
        remove_roles_id = [role.id for role in set(before.roles) - set(after.roles)]
        userdb = session.query(User).filter_by(userid=after.id).first()
        if config.roles.serverbooster in remove_roles_id:
            if userdb.level < 15:
                await after.remove_roles(after.guild.get_role(config.roles.mcmd_5lv))
            if userdb.level < 5:
                await after.remove_roles(after.guild.get_role(config.roles.mcmd_15lv))


async def setup(bot: commands.Bot):
    await bot.add_cog(CWelcome(bot))
