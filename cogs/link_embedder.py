import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CTemplate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if "https://discord.com/channels/" in message.content:
            # メッセージリンクが含まれている場合
            try:
                link = (
                    message.content.split("https://discord.com/channels/")[1]
                    .split(" ")[0]
                    .split("\n")[0]
                )
                guild_id, channel_id, message_id = map(int, link.split("/"))
            except Exception:
                return

            # メッセージリンクが現在のサーバーに属しているかどうかをチェック
            if message.guild.id != guild_id:
                # 現在のサーバー以外のリンクには反応しない
                return

            try:
                # リンク先のメッセージオブジェクトを取得
                target_channel = self.bot.get_guild(guild_id).get_channel(channel_id)
                target_message = await target_channel.fetch_message(message_id)

                # リンク先のメッセージオブジェクトから、メッセージの内容、送信者の名前とアイコンなどの情報を取得
                content = target_message.content
                author = target_message.author
                name = author.name
                icon_url = (
                    author.avatar.url if author.avatar else author.default_avatar.url
                )
                timestamp = target_message.created_at
                target_message_link = (
                    f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
                )

                if content == "":
                    content = "本文なし"

                # Embedオブジェクトを作成
                embed = discord.Embed(
                    description=content, color=0x00BFFF, timestamp=timestamp
                )
                embed.set_author(name=name, icon_url=icon_url)
                embed.set_footer(text=f"From #{target_message.channel}")

                # 画像添付ファイルがある場合、最初の画像をEmbedに追加
                if target_message.attachments:
                    attachment = target_message.attachments[0]  # 最初の添付ファイルを取得
                    if any(
                        attachment.filename.lower().endswith(image_ext)
                        for image_ext in ["png", "jpg", "jpeg", "gif", "webp"]
                    ):
                        embed.set_image(url=attachment.url)  # 画像をEmbedに設定

                # ボタンコンポーネントを使ったViewオブジェクトを作成
                view = discord.ui.View(timeout=None)
                view.add_item(
                    discord.ui.Button(
                        label="メッセージ先はこちら",
                        style=discord.ButtonStyle.link,
                        url=target_message_link,
                    )
                )

                # EmbedとViewをメッセージとして送信
                await message.channel.send(embed=embed, view=view)

                # リンク先のメッセージがembedだった場合は、元のembedも表示する
                for original_embed in target_message.embeds:
                    await message.channel.send(embed=original_embed, view=view)

            except Exception as e:
                logger.error(f"エラーらしい: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CTemplate(bot))
