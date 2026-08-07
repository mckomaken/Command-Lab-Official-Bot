import discord
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View, button

from config.config import config
from database import User, session

# 認証回答者


class RequestCheckButton(View):
    def __init__(self, userid):
        super().__init__(timeout=None)
        self.userid = userid

    @button(label="承認", style=ButtonStyle.success, custom_id="admin_check")
    async def admin_rule_check_agree_button(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await member.add_roles(interaction.guild.get_role(config.roles.authenticated_respondent))
            await interaction.response.send_message(embed=discord.Embed(title="承認", description=f"{member.mention}にロールを付与しました。\n\n-# 実行者: {interaction.user.mention}", color=discord.Color.green()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証回答者ロール: 承認", description="あなたの認証回答者ロール付与申請が承認されました。", color=discord.Color.green()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="却下", style=ButtonStyle.grey, custom_id="admin_reject")
    async def admin_rule_reject_button(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await interaction.response.send_message(embed=discord.Embed(title="否認", description=f"{member.mention}の申請が否認されました。\n\n-# 実行者: {interaction.user.mention}", color=discord.Color.red()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証回答者ロール: 否認", description="あなたの認証回答者ロール付与申請は否認されました", color=discord.Color.red()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="削除", style=ButtonStyle.danger, custom_id="admin_delete")
    async def admin_rule_delete_button(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class RequestButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="申請する", style=ButtonStyle.success, custom_id="request")
    async def requestbutton(self, interaction: Interaction, button: Button):
        view = RequestCheckButton(userid=interaction.user.id)
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        admin_channel = await interaction.guild.fetch_channel(config.channels.admin_meeting)
        admin_embed = discord.Embed(
            title="認証回答者ロール付与申請",
            description=f"ユーザー: {interaction.user.mention}\nユーザー名: {interaction.user.name}\nユーザーID: {interaction.user.id}\nコマ研レベル: {userdb.level}.{userdb.exp}\n有効チャット数: {userdb.chatcount}",
            color=discord.Color.orange()
        )
        await admin_channel.send(embed=admin_embed, view=view)

        await interaction.response.send_message("申請が完了しました。\n承認/否認結果は後ほどDMにてお知らせいたします。\n-# BotからのDM受信を許可しておいてください", ephemeral=True)


class CAuthenticatedRespondent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="authenticated-respondent-request", description="認証回答者ロール付与申請コマンド")
    async def authenticated_respondent_request(self, interaction: Interaction):
        role = interaction.guild.get_role(config.roles.authenticated_respondent)
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        if role in interaction.user.roles:
            await interaction.response.send_message("あなたは既に認証回答者の為、申請することはできません", ephemeral=True)
            return
        elif userdb.level < 20 or not userdb:
            await interaction.response.send_message("あなたはコマ研レベル20Lv未満の為、申請することはできません", ephemeral=True)
            return
        request_embed = discord.Embed(
            description="# `認証回答者ロール`付与申請を行いますか？\n\n運営が申請者を確認し、承認されると`認証回答者ロール`が付与されます。\n\n申請を行う場合は以下のボタンを押してください。",
            color=discord.Color.green()
        )
        view = RequestButton()
        await interaction.response.send_message(embed=request_embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CAuthenticatedRespondent(bot))
    bot.add_view(RequestButton())
    bot.add_view(RequestCheckButton(userid=None))
