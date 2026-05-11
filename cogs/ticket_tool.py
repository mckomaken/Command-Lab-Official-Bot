import discord
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View, button
from datetime import datetime

from config.config import config


class ResumeButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="【運営用】問い合わせを再開", style=ButtonStyle.green, custom_id="resume")
    async def resumebutton(self, interaction: Interaction, button: Button):
        await interaction.channel.edit(locked=False)
        await interaction.message.delete()
        await interaction.response.send_message("問い合わせを再開しました")


class FinalFinishButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="はい(終了する)", style=ButtonStyle.green, custom_id="final-finish-yes")
    async def finalfinishbutton_yes(self, interaction: Interaction, button: Button):
        try:
            resumebutton = ResumeButton()
            await interaction.response.send_message("問い合わせを終了しました", view=resumebutton)
        except Exception as e:
            print(e)
        await interaction.message.delete()
        await interaction.channel.edit(locked=True)

    @button(label="いいえ(終了しない)", style=ButtonStyle.red, custom_id="final-finish-no")
    async def finalfinishbutton_no(self, interaction: Interaction, button: Button):
        await interaction.message.delete()


class FinidhButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="問い合わせを終了する", style=ButtonStyle.red, custom_id="finish")
    async def finishbutton(self, interaction: Interaction, button: Button):
        finalfinishbutton = FinalFinishButton()
        await interaction.response.send_message("本当に問い合わせを終了してもいいですか？", view=finalfinishbutton)


class ContactButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="問い合わせを開始する", style=ButtonStyle.success, custom_id="contact")
    async def contactbutton(self, interaction: Interaction, button: Button):
        thread_title = f"{interaction.user.display_name}-{datetime.now().strftime("%Y%m%d%H%M%S")}"
        thread = await interaction.channel.create_thread(name=thread_title, invitable=False, auto_archive_duration=4320)
        contact_log = await interaction.guild.fetch_channel(config.channels.cmdbot_log)
        thread_embed = discord.Embed(
            title="問い合わせが開始されました。",
            description="問い合わせ内容を記入してお待ちください\n運営が気づき次第、対応いたします。"
        )
        thread_embed.set_footer(text="間違えて作成した場合は下のボタンを押してください")
        admin_role = f"\n<@&{config.roles.administrater}> 対応お願いします"
        finidhbutton = FinidhButton()
        await contact_log.send(f"問い合わせが開始されました{thread.jump_url}")
        await thread.send(f"問い合わせ者:{interaction.user.mention}{admin_role}", embed=thread_embed, view=finidhbutton)
        await interaction.response.send_message(f"{thread.jump_url}を作成しました。そちらへ移動願います", ephemeral=True)


class TicketTool(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="contact", description="問い合わせ開始メッセージを送信")
    async def contact(self, interaction: discord.Interaction):
        contact_embed = discord.Embed(
            title="お問い合わせ",
            description="鯖主へ個別に問い合わせしたい場合は、下の緑のボタンを押してください。",
            color=0x30ff00
        )
        try:
            button = ContactButton()
            await interaction.channel.send(embed=contact_embed, view=button, silent=True)
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketTool(bot))
    bot.add_view(ResumeButton())
    bot.add_view(FinalFinishButton())
    bot.add_view(FinidhButton())
    bot.add_view(ContactButton())
