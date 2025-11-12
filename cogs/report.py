import random
import string
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from config.config import config


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

    async def CallBack(self, interaction: discord.Interaction):
        reason_map = {
            "dont-like": "内容が気に入らない(その他)",
            "discord-violation": "Discordの各種規約違反",
            "law-violation": "その他法令・規約違反",
            "off-topic": "チャンネルの趣旨に合わない",
            "harass": "誹謗中傷・差別・脅迫",
            "negative-language": "強い言葉づかい・否定的表現",
            "nsfw": "暴力的・エロ・グロ",
            "spam": "荒らし・スパム",
            "politics-religion": "政治・宗教的活動",
            "exposing-information": "個人情報の過度な詮索・漏洩",
            "mention": "無意味なメンション",
            "inappropriate-profile": "不適切な名前・画像・鯖タグ",
            "advertising-rule-violation": "宣伝ルール違反",
            "question-rule-violation": "質問ルール違反",
            "impersonation": "他参加者へのなりすまし"
        }

        reason = reason_map.get(self.values[0], "不明な理由")
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
            callback=self.SendMessage
        )
        self.bot.tree.add_command(self.context_menu)

    async def SendMessage(self, interaction: discord.Interaction, message: discord.Message) -> None:
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
                discord.SelectOption(label="その他法令・規約違反", value="law-violation"),
                discord.SelectOption(label="チャンネルの趣旨に合わない", value="off-topic"),
                discord.SelectOption(label="誹謗中傷・差別・脅迫", value="harass"),
                discord.SelectOption(label="強い言葉づかい・否定的表現", value="negative-language"),
                discord.SelectOption(label="暴力的・エロ・グロ", value="nsfw"),
                discord.SelectOption(label="荒らし・スパム", value="spam"),
                discord.SelectOption(label="政治・宗教的活動", value="politics-religion"),
                discord.SelectOption(label="個人情報の過度な詮索・漏洩", value="exposing-information"),
                discord.SelectOption(label="無意味なメンション", value="mention"),
                discord.SelectOption(label="不適切な名前・画像・鯖タグ", value="inappropriate-profile"),
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
