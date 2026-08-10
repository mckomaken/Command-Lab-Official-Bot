import discord
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View, button

from config.config import config
from database import User, session


class RequestCheckButton4(View):
    def __init__(self, userid, admin_user_name1, admin_user_name2):
        super().__init__(timeout=None)
        self.userid = userid
        self.admin_user_name1 = admin_user_name1
        self.admin_user_name2 = admin_user_name2

    @button(label="承認1", style=ButtonStyle.success, custom_id="admin_request_check41", row=0, disabled=True)
    async def admin_authenticated_respondent_request_check_agree_button41(self, interaction: Interaction, button: Button):
        return

    @button(label="承認2", style=ButtonStyle.success, custom_id="admin_request_check42", row=0)
    async def admin_authenticated_respondent_request_check_agree_button42(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await member.add_roles(interaction.guild.get_role(config.roles.authenticated_respondent))
            await interaction.response.send_message(embed=discord.Embed(title="承認", description=f"{member.mention}にロールを付与しました。\n\n-# {self.admin_user_name1}\n-# {self.admin_user_name2}\n-# 承認2: {interaction.user.display_name}", color=discord.Color.green()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証済み回答者ロール: 承認", description="あなたの認証済み回答者ロール付与申請が承認されました。", color=discord.Color.green()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="却下1", style=ButtonStyle.grey, custom_id="admin_request_reject41", row=1, disabled=True)
    async def admin_authenticated_respondent_request_reject_button41(self, interaction: Interaction, button: Button):
        return

    @button(label="却下2", style=ButtonStyle.grey, custom_id="admin_request_reject42", row=1)
    async def admin_authenticated_respondent_request_reject_button42(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await interaction.response.send_message(embed=discord.Embed(title="否認", description=f"{member.mention}の申請が否認されました。\n\n-# {self.admin_user_name1}\n-# {self.admin_user_name2}\n-# 却下2: {interaction.user.display_name}", color=discord.Color.red()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証済み回答者ロール: 否認", description="あなたの認証済み回答者ロール付与申請は否認されました", color=discord.Color.red()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="削除", style=ButtonStyle.danger, custom_id="admin_delete", row=2)
    async def admin_authenticated_respondent_request_delete_button(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class RequestCheckButton3(View):
    def __init__(self, userid, admin_user_name1):
        super().__init__(timeout=None)
        self.userid = userid
        self.admin_user_name1 = admin_user_name1

    @button(label="承認1", style=ButtonStyle.success, custom_id="admin_request_check31", row=0)
    async def admin_authenticated_respondent_request_check_agree_button31(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton4(userid=interaction.user.id, admin_user_name1=self.admin_user_name1, admin_user_name2=f"承認1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("承認しました。", ephemeral=True)
        return

    @button(label="承認2", style=ButtonStyle.success, custom_id="admin_request_check32", row=0)
    async def admin_authenticated_respondent_request_check_agree_button32(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton4(userid=interaction.user.id, admin_user_name1=self.admin_user_name1, admin_user_name2=f"承認1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("承認しました。", ephemeral=True)
        return

    @button(label="却下1", style=ButtonStyle.grey, custom_id="admin_request_reject31", row=1, disabled=True)
    async def admin_authenticated_respondent_request_reject_button31(self, interaction: Interaction, button: Button):
        return

    @button(label="却下2", style=ButtonStyle.grey, custom_id="admin_request_reject32", row=1)
    async def admin_authenticated_respondent_request_reject_button32(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await interaction.response.send_message(embed=discord.Embed(title="否認", description=f"{member.mention}の申請が否認されました。\n\n-# {self.admin_user_name1}\n-# 却下2: {interaction.user.display_name}", color=discord.Color.red()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証済み回答者ロール: 否認", description="あなたの認証済み回答者ロール付与申請は否認されました", color=discord.Color.red()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="削除", style=ButtonStyle.danger, custom_id="admin_delete", row=2)
    async def admin_authenticated_respondent_request_delete_button(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class RequestCheckButton2(View):
    def __init__(self, userid, admin_user_name1):
        super().__init__(timeout=None)
        self.userid = userid
        self.admin_user_name1 = admin_user_name1

    @button(label="承認1", style=ButtonStyle.success, custom_id="admin_request_check21", row=0, disabled=True)
    async def admin_authenticated_respondent_request_check_agree_button21(self, interaction: Interaction, button: Button):
        return

    @button(label="承認2", style=ButtonStyle.success, custom_id="admin_request_check22", row=0)
    async def admin_authenticated_respondent_request_check_agree_button22(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        try:
            member = interaction.guild.get_member(self.userid)
            await member.add_roles(interaction.guild.get_role(config.roles.authenticated_respondent))
            await interaction.response.send_message(embed=discord.Embed(title="承認", description=f"{member.mention}にロールを付与しました。\n\n-# {self.admin_user_name1}\n-# 承認2: {interaction.user.display_name}", color=discord.Color.green()))
            await interaction.message.edit(view=None)
            await member.send(embed=discord.Embed(title="認証済み回答者ロール: 承認", description="あなたの認証済み回答者ロール付与申請が承認されました。", color=discord.Color.green()))
        except Exception as e:
            await interaction.response.send_message(f"エラーが発生しました: \n{e}", ephemeral=True)
            return

    @button(label="却下1", style=ButtonStyle.grey, custom_id="admin_request_reject21", row=1)
    async def admin_authenticated_respondent_request_reject_button21(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton4(userid=interaction.user.id, admin_user_name1=self.admin_user_name1, admin_user_name2=f"却下1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("却下しました。", ephemeral=True)
        return

    @button(label="却下2", style=ButtonStyle.grey, custom_id="admin_request_reject22", row=1)
    async def admin_authenticated_respondent_request_reject_button22(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton4(userid=interaction.user.id, admin_user_name1=self.admin_user_name1, admin_user_name2=f"却下1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("却下しました。", ephemeral=True)
        return

    @button(label="削除", style=ButtonStyle.danger, custom_id="admin_delete", row=2)
    async def admin_authenticated_respondent_request_delete_button(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class RequestCheckButton1(View):
    def __init__(self, userid):
        super().__init__(timeout=None)
        self.userid = userid

    @button(label="承認1", style=ButtonStyle.success, custom_id="admin_request_check11", row=0)
    async def admin_authenticated_respondent_request_check_agree_button11(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton2(userid=self.userid, admin_user_name1=f"承認1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("承認しました。", ephemeral=True)
        return

    @button(label="承認2", style=ButtonStyle.success, custom_id="admin_request_check12", row=0)
    async def admin_authenticated_respondent_request_check_agree_button12(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton2(userid=self.userid, admin_user_name1=f"承認1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("承認しました。", ephemeral=True)
        return

    @button(label="却下1", style=ButtonStyle.grey, custom_id="admin_request_reject11", row=1)
    async def admin_authenticated_respondent_request_reject_button11(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton3(userid=self.userid, admin_user_name1=f"却下1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("却下しました。", ephemeral=True)
        return

    @button(label="却下2", style=ButtonStyle.grey, custom_id="admin_request_reject12", row=1)
    async def admin_authenticated_respondent_request_reject_button12(self, interaction: Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            return
        view = RequestCheckButton3(userid=self.userid, admin_user_name1=f"却下1: {interaction.user.display_name}")
        await interaction.message.edit(view=view)
        await interaction.response.send_message("却下しました。", ephemeral=True)
        return

    @button(label="削除", style=ButtonStyle.danger, custom_id="admin_delete", row=2)
    async def admin_authenticated_respondent_request_delete_button(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class RequestButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="申請する", style=ButtonStyle.success, custom_id="request")
    async def requestbutton(self, interaction: Interaction, button: Button):
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        role = interaction.guild.get_role(config.roles.authenticated_respondent)
        if role in interaction.user.roles:
            await interaction.response.send_message("あなたは既に認証済み回答者の為、申請することはできません", ephemeral=True)
            return
        elif userdb.level < 20 or not userdb:
            await interaction.response.send_message("あなたはコマ研レベル20Lv未満の為、申請することはできません", ephemeral=True)
            return
        view = RequestCheckButton1(userid=interaction.user.id)
        admin_channel = await interaction.guild.fetch_channel(config.channels.admin_meeting)
        admin_embed = discord.Embed(
            title="認証済み回答者ロール付与申請",
            description=f"ユーザー: {interaction.user.mention}\nユーザー名: {interaction.user.name}\nユーザーID: {interaction.user.id}\nコマ研レベル: {userdb.level}.{userdb.exp}\n有効チャット数: {userdb.chatcount}",
            color=discord.Color.orange()
        )
        await admin_channel.send(embed=admin_embed, view=view)

        await interaction.response.send_message("申請が完了しました。\n承認/否認結果は後ほどDMにてお知らせいたします。\n-# BotからのDM受信を許可しておいてください", ephemeral=True)


class CAuthenticatedRespondent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="authenticated-respondent-request", description="認証済み回答者ロール付与申請コマンド")
    async def authenticated_respondent_request(self, interaction: Interaction):
        role = interaction.guild.get_role(config.roles.authenticated_respondent)
        userdb = session.query(User).filter_by(userid=interaction.user.id).first()
        if role in interaction.user.roles:
            await interaction.response.send_message("あなたは既に認証済み回答者の為、申請することはできません", ephemeral=True)
            return
        elif userdb.level < 20 or not userdb:
            await interaction.response.send_message("あなたはコマ研レベル20Lv未満の為、申請することはできません", ephemeral=True)
            return
        request_embed = discord.Embed(
            description="# `認証済み回答者ロール`付与申請を行いますか？\n\n運営が申請者を確認し、承認されると`認証済み回答者ロール`が付与されます。\n\n申請を行う場合は以下のボタンを押してください。",
            color=discord.Color.green()
        )
        view = RequestButton()
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=request_embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(embed=request_embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CAuthenticatedRespondent(bot))
    bot.add_view(RequestButton())
    bot.add_view(RequestCheckButton1(userid=None))
