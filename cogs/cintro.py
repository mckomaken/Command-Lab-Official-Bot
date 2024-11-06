import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Item, View, button

from config.config import config


class IntroView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(emoji="🗑️", custom_id="delete", style=discord.ButtonStyle.gray)
    async def _remove(self, interaction: Interaction, item: Item):
        await interaction.response.defer(thinking=True, ephemeral=True)
        old_message_id = interaction.message.reference.message_id
        old_message = await interaction.channel.fetch_message(old_message_id)
        if old_message is None:
            await interaction.followup.send(
                content="メッセージ情報がないから消去できないよ!!!", ephemeral=True
            )
        member_id = old_message.author.id
        member = await interaction.guild.fetch_member(member_id)
        if member is None:
            await interaction.followup.send(
                "削除したよ\n送り主が既にサーバーにいなかったから誰でも消せるようになってるよ",
                ephemeral=True,
            )
            await interaction.message.delete()
        elif member_id == interaction.user.id:
            await interaction.followup.send(content="削除したよ", ephemeral=True)
            await interaction.message.delete()
        else:
            if member.resolved_permissions.manage_messages:
                await interaction.message.delete()
            else:
                await interaction.followup.send(
                    content="権限がないから消去できないよ", ephemeral=True
                )


class CIntro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        elif message.channel.id in config.question_channels:
            org_msg = message
            counter = 0
            for i in config.question_channels:
                q_ch = message.guild.get_channel(i)
                if q_ch.type == discord.ChannelType.forum:
                    for j in q_ch.threads:
                        async for message in j.history(limit=200):
                            if message.author == org_msg.author:
                                counter += 1
                else:
                    async for message in q_ch.history(limit=200):
                        if message.author == org_msg.author:
                            counter += 1
            if counter == 1:
                embed = discord.Embed(
                    title="質問する前に確認して！",
                    description="**これはコマ研サーバーで直近で質問チャンネルで質問をしたことがない人向けに送られています。**\n"
                    + "### 回答者があなたの望む答えを出せるように質問文で以下の内容が含まれているか確認してください。\n"
                    + "- **`どんなコマンドを打ったのか（コマンドを打ったが実行されない！という質問のみ）`**\n"
                    + "- **`データパック/チャット/コマブロのどれでコマンドを実行したか（コマンドを打ったが実行されない！という質問のみ）`**\n"
                    + "- **`何をしたいのか（一番重要）`**\n \n"
                    + "**思考を文字なしで共有しているわけでもないしこのサーバーにいるみんながあなたと同じ考えをしているわけありません。**\n"
                    + "**困ったときはお互い様です。どうしたらなにができないか、きちんと書いてください。**",
                    color=0xE06E64,
                )
                embed.set_footer(
                    text="もしこのメッセージが誤送信/既にメッセージの通りに質問を書いた場合は下の「🗑️」からメッセージを削除してください。\n"
                    + "ボタンは返信元のユーザーにしか実行されません"
                )
                view = IntroView()
                await org_msg.reply(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CIntro(bot))
    bot.add_view(IntroView())
