from discord.ext import commands
import discord

# 正規メンバーのロールid
role_id = 965075508721238067

# 総合雑談のチャンネルid
channel_id = 965069665388867624

class CWelcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # メンバーの状態変化を検知するイベント
    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before:discord.Member, after:discord.Member):

        added_roles_id = [role.id for role in set(after.roles) - set(before.roles)] # 増えたロールのid一覧
        if role_id in added_roles_id:
            
            channel = await self.bot.fetch_channel(channel_id)
            await channel.send(f"{after.mention}さんが入所しました。コマ研へようこそ！")
            

async def setup(bot: commands.Bot):
    await bot.add_cog(CWelcome(bot))