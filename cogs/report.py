import discord
from discord.ext import commands
from discord import app_commands
import random
import string
from config.config import config
from datetime import datetime


class Select(discord.ui.Select):
    def __init__(self, placeholder: str, options: list[discord.SelectOption], min_values: int, max_values: int, custom_id: str, bot: commands.Bot, message: discord.Message):
        super().__init__(
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values,
            custom_id=custom_id
        )
        self.bot = bot
        self.message = message

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "dont-like":
            reason = "内容が気に入らない(その他)"
        elif self.values[0] == "discord-violation":
            reason = "Discordの各種規約違反"
        elif self.values[0] == "law-violation":
            reason = "Discord以外の各種法令・規約違反"
        elif self.values[0] == "off-topic":
            reason = "チャンネルの趣旨に合わない内容"
        elif self.values[0] == "harass":
            reason = "誹謗中傷・差別・脅迫"
        elif self.values[0] == "negative-language":
            reason = "強い言葉づかい・過度な否定的表現"
        elif self.values[0] == "nsfw":
            reason = "暴力的・卑猥・グロテスクな内容"
        elif self.values[0] == "spam":
            reason = "荒らし・スパム"
        elif self.values[0] == "politics-religion":
            reason = "政治・宗教的活動"
        elif self.values[0] == "exposing-information":
            reason = "個人情報の過度な詮索・漏洩"
        elif self.values[0] == "mention":
            reason = "無意味なメンション"
        elif self.values[0] == "inappropriate-profile":
            reason = "不適切な名前・プロフ画像・サーバータグ"
        elif self.values[0] == "advertising-rule-violation":
            reason = "宣伝ルール違反"
        elif self.values[0] == "question-rule-violation":
            reason = "質問ルール違反"
        elif self.values[0] == "impersonation":
            reason = "他参加者へのなりすまし"

        important_logch = await self.bot.fetch_channel(config.admin_meeting_ch)
        REPORTMESSAGE = f"""
`通報内容:`{reason}
`送信者　:`{self.message.author.mention}
`ＵＲＬ　:`{self.message.jump_url}
### メッセージ内容
{self.message.content if self.message.content else "メッセージ本文なし"}
"""
        report_embed = discord.Embed(
            title="通報を受け付けました",
            description=REPORTMESSAGE,
            color=0x80ff00
        )
        report_embed.set_image(url=self.message.attachments[0].url if self.message.attachments else None)
        report_embed.set_author(name=interaction.user.display_name, icon_url=f"https://cdn.discordapp.com/embed/avatars/{random.randint(0, 5)}.png" if interaction.user.avatar is None else interaction.user.avatar.url)
        report_embed.set_footer(text=f"通報ID: {self.custom_id}")

        REPORTLOGMESSAGE = f"""
`通報内容:`{reason}
`送信日時:`{self.message.created_at.strftime('%Y/%m/%d %H:%M:%S')}
`通報日時:`{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
`通報者　:`{interaction.user.mention}/{interaction.user.id}
`送信者　:`{self.message.author.mention}/{self.message.author.id}
`ＵＲＬ　:`{self.message.jump_url}/{self.message.id}
### メッセージ内容
{self.message.content if self.message.content else "メッセージ本文なし"}
"""
        report_log_embed = discord.Embed(
            title="通報がありました",
            description=REPORTLOGMESSAGE,
            color=0xff00ff
        )
        report_log_embed.set_image(url=self.message.attachments[0].url if self.message.attachments else None)
        report_log_embed.set_footer(text=f"通報ID: {self.custom_id}")
        await important_logch.send(embed=report_log_embed)
        await interaction.response.edit_message(embed=report_embed, view=None)


class Report(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.context_menu = app_commands.ContextMenu(
            name="このメッセージを通報",
            callback=self.send_msg
        )
        self.bot.tree.add_command(self.context_menu)

    async def send_msg(self, interaction: discord.Interaction, message: discord.Message) -> None:
        random_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))

        embed = discord.Embed(
            description="最も当てはまる通報内容を以下の選択肢から1つ選んでください",
            color=0xff0000
        )
        options = Select(
            placeholder="違反内容を選択してください",
            options=[
                discord.SelectOption(label="内容が気に入らない(その他)", value="dont-like"),
                discord.SelectOption(label="Discordの各種規約違反", value="discord-violation"),
                discord.SelectOption(label="Discord以外の各種法令・規約違反", value="law-violation"),
                discord.SelectOption(label="チャンネルの趣旨に合わない内容", value="off-topic"),
                discord.SelectOption(label="誹謗中傷・差別・脅迫", value="harass"),
                discord.SelectOption(label="強い言葉づかい・過度な否定的表現", value="negative-language"),
                discord.SelectOption(label="暴力的・卑猥・グロテスクな内容", value="nsfw"),
                discord.SelectOption(label="荒らし・スパム", value="spam"),
                discord.SelectOption(label="政治・宗教的活動", value="politics-religion"),
                discord.SelectOption(label="個人情報の過度な詮索・漏洩", value="exposing-information"),
                discord.SelectOption(label="無意味なメンション", value="mention"),
                discord.SelectOption(label="不適切な名前・プロフ画像・サーバータグ", value="inappropriate-profile"),
                discord.SelectOption(label="宣伝ルール違反", value="advertising-rule-violation"),
                discord.SelectOption(label="質問ルール違反", value="question-rule-violation"),
                discord.SelectOption(label="他参加者へのなりすまし", value="impersonation")
            ],
            min_values=1,
            max_values=1,
            custom_id=f"{random_id}-{message.id}",
            bot=self.bot,
            message=message
        )
        view = discord.ui.View()
        view.add_item(options)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
