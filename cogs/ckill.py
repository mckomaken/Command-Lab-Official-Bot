import io
import json
import os
import random
from typing import Optional

import discord
from discord import Member, app_commands
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
from PIL import Image, ImageDraw, ImageFont


def escape(text: str) -> str:
    return escape_markdown(escape_mentions(text), as_needed=True)


class CKill(commands.Cog):
    lang_data: dict[str, str]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # 最大数設定
        self.max_count = 10

    def generate_image(self, msg: str) -> discord.File:
        img = Image.open("./assets/death_screen_bg.png").convert("RGBA")
        filter_img = Image.new("RGBA", size=img.size, color=0xff0000ff)
        img = Image.blend(img, filter_img, 0.2)

        draw = ImageDraw.Draw(img)

        def unifont(size: int):
            return ImageFont.truetype(os.path.join(os.getenv("BASE_DIR", "."), "assets/mcfont.ttf"), size)

        def drawtext(text: str, y: float, size: int):
            draw.text(((img.width / 2) - (draw.textlength(text, font=unifont(size)) / 2) + 1, y + 2), text, fill=0x42424201, font=unifont(size))
            draw.text(((img.width / 2) - (draw.textlength(text, font=unifont(size)) / 2) - 1, y), text, fill=0xffffffff, font=unifont(size))

        drawtext("死んでしまった！", 256, 74)
        drawtext(msg, 364, 32)
        drawtext(f"スコア：{random.randint(1, 9999)}", 428, 32)

        respawn_button = Image.open("./assets/button-respawn.png").convert("RGBA")
        title_button = Image.open("./assets/button-title.png").convert("RGBA")

        img.paste(respawn_button, (560, 563))
        img.paste(title_button, (560, 659))

        stream = io.BytesIO()
        img.save(stream, "WEBP")
        file = discord.File(io.BytesIO(stream.getvalue()), filename="preview.webp")

        return file

    def generate_death_log(self, victim: Optional[str], player: str) -> str:
        death_logs = self.death_logs

        # 指定なし -> 1人のみのdeath log
        if victim is None:
            death_logs = [t for t in self.death_logs if "%2$s" not in t]
            victim = ""
        else:
            victim, player = player, victim

        # キルログ生成
        return random.choice(death_logs) \
            .replace("%1$s", escape(player)) \
            .replace("%2$s", escape(victim)) \
            .replace("%3$s", f"[{random.choice(self.items)}]")

    @app_commands.command(name="ckill", description="キルコマンド(ネタ)")
    @app_commands.describe(target="キルするユーザー(任意)", count="回数(デフォルト1)")
    async def ckill(
        self, interaction: discord.Interaction,
        target: Optional[Member] = None,
        count: Optional[int] = 1
    ):
        target_name = None
        if target:
            target_name = escape(target.display_name)

        # 最大数制限
        if 0 < count <= self.max_count:
            logs: list[str] = []
            for _ in range(count):
                logs.append(self.generate_death_log(
                    target_name,
                    escape(interaction.user.display_name)
                ))


            await interaction.response.send_message(
                "\n".join(logs).rstrip("\n"),
                allowed_mentions=discord.AllowedMentions.none(),
                file=self.generate_image(logs[-1])
            )
        else:
            await interaction.response.send_message(
                f"countには{self.max_count}以下の自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪",
                ephemeral=True
            )

    async def cog_load(self) -> None:
        # jsonファイル を dict(lang_data) に変換
        with open(file='./assets/ja_jp.json', mode='r', encoding='utf-8') as file:
            self.lang_data = json.load(file)

            self.death_logs = [v for k, v in self.lang_data.items() if "death." in k]
            self.entities = [
                v.replace("のスポーンエッグ", "") for k, v in self.lang_data.items()
                if "item.minecraft." in k and "_spawn_egg" in k
            ]
            self.items = [v for k, v in self.lang_data.items() if "item.minecraft." in k]


async def setup(bot: commands.Bot):
    await bot.add_cog(CKill(bot))
