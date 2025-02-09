import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Item, View, button

from config.config import config

QDESC = """
**⚠️このメッセージは直近で質問チャンネル内で発言したことがない人向けに自動で送信されます⚠️**
## みんながあなたの質問にきちんと答えられるように、以下の要素が含まれているか確認してね
> **マイクラのバージョンを書いてますか？【必須】**
> -# 一部コマンドはバージョンによって記述がガラっと変わります
> -# 絶対に書いてください
> **抽象的な表現 / 作業を他人に1から任せようとしてませんか？**
> -# 何をしたいか秘密にしたいからといって具体的に書かずに質問してませんか？
> -# 「こういうシステムを作りたいです。コマンドを教えてください。」みたいに、作業を他人に全部任せようとしてませんか？
> -# こういう質問は無視されやすいです。秘密にしようとせず、やりたいことをちゃんと書いてください
> -# また、一度やりたいことを調べ、自作してみてください。そこから、わからなかったところを聞いてみてください
> -# なお作成の依頼をしたい場合は <#965076561466363954> か <#965076515500994630> で言ってください(基本的に作られません)
> **何を使用してコマンドを打ってますか？**
> -# データパックで書いたのかコマブロで書いたのかチャットで書いたのかで結果が変わるコマンドがあります**

急いでるかもしれませんが、とりあえず頭に思い浮かんだ言葉を入れても伝わらなければなんともなりません。
一旦息を吸って、吐いて、自分の質問を見直してみてください。

-# 因みに、<#965085268338176081> や <#965085298537144380> も見てみてください。コマンドの作成に便利なサイトが載ってるかも...
"""
QFOOTER = """
このメッセージは🗑️を押すことで削除ができます。
ボタンは返信元のユーザーのみ利用可能です。
"""


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
                "削除したよ\n送り主が既にサーバーにいなかったから誰でも消せるようになってるよ", ephemeral=True
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
                    description=QDESC,
                    color=0xE06E64,
                )
                embed.set_footer(
                    text=QFOOTER
                )
                view = IntroView()
                await org_msg.reply(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CIntro(bot))
    bot.add_view(IntroView())
