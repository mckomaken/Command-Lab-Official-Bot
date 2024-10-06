import io
import json
import os
import zipfile
from datetime import datetime

import aiofiles
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image

from config import config
from schemas.data import Blocks, DataPaths, Items
from utils.util import create_codeblock


class CItem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="citem", description="アイテムを検索します")
    @app_commands.describe(id="アイテムまたはブロックID")
    @app_commands.guild_only()
    async def citem(self, interaction: discord.Interaction, id: str):
        async with aiofiles.open("./minecraft_data/data/dataPaths.json") as fp:
            dataPath = DataPaths.model_validate_json(await fp.read())

            async with aiofiles.open(
                "./minecraft_data/data/" + dataPath.pc[config.latest_version].items + "/items.json"
            ) as fp:
                async with aiofiles.open(
                    "./minecraft_data/data/" + dataPath.pc[config.latest_version].blocks + "/blocks.json"
                ) as fp2:
                    items = Items.model_validate_json(await fp.read())
                    blocks = Blocks.model_validate_json(await fp2.read())
                    for item in items.root:
                        if item.name == id.replace("minecraft:", ""):

                            is_item = id not in [b.name for b in blocks.root]
                            block = next(
                                iter([b for b in blocks.root if b.name == item.name]),
                                None,
                            )

                            async with aiofiles.open(
                                os.path.join(os.getenv("TMP_DIRECTORY", "./.tmp"), "ja_jp.json"),
                                mode="rb",
                            ) as lang_fp:
                                with zipfile.ZipFile(
                                    os.path.join(
                                        os.getenv("TMP_DIRECTORY", "./.tmp"),
                                        f"client_{config.latest_version}.jar",
                                    )
                                ) as zipfp:
                                    tn = "item" if is_item else "block"
                                    lang_data = json.loads(await lang_fp.read())
                                    lang_text = lang_data[f"{tn}.minecraft.{item.name}"]
                                    with zipfp.open(f"assets/minecraft/textures/{tn}/{id}.png") as imgfp:
                                        img = Image.open(imgfp).resize((256, 256), Image.Resampling.NEAREST)
                                        streamimg = io.BytesIO()
                                        img.save(streamimg, "WEBP")
                                        file = discord.File(
                                            io.BytesIO(streamimg.getvalue()),
                                            filename=f"{id}.webp",
                                        )
                                        files = [file]
                                        embed = discord.Embed(
                                            title=lang_text,
                                            description=create_codeblock("minecraft:" + item.name),
                                            timestamp=datetime.now(),
                                        )
                                        embed.add_field(
                                            name="最大スタック数",
                                            value=create_codeblock(f"{item.stackSize}"),
                                        )

                                        if block is not None:
                                            if block.boundingBox != "empty":
                                                embed.add_field(
                                                    name="爆破耐性",
                                                    value=create_codeblock(block.resistance),
                                                )
                                                embed.add_field(
                                                    name="硬度",
                                                    value=create_codeblock(block.hardness),
                                                )

                                            if block.material == "mineable/pickaxe":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("ピッケル"),
                                                )
                                            elif block.material == "mineable/axe":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("斧"),
                                                )
                                            elif block.material == "mineable/shovel":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("シャベル"),
                                                )
                                            elif block.material == "mineable/hoe":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("クワ"),
                                                )
                                            elif block.material == "wool":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("ハサミ"),
                                                )
                                            elif block.material == "coweb":
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("剣"),
                                                )
                                            else:
                                                embed.add_field(
                                                    name="適正ツール",
                                                    value=create_codeblock("素手"),
                                                )

                                            di_imgs = Image.new("RGBA", (1000, 64), 0x000000FF)
                                            for d in block.drops:
                                                if drop_item := next(
                                                    iter([di for di in items.root if di.id == d]),
                                                    None,
                                                ):
                                                    di_is_item = drop_item.name not in [b.name for b in blocks.root]
                                                    ci = 8
                                                    di_typename = "item" if di_is_item else "block"
                                                    with zipfp.open(
                                                        f"assets/minecraft/textures/{di_typename}/{drop_item.name}.png"
                                                    ) as imgfp2:
                                                        ci += 68
                                                        di_imgs.paste(
                                                            Image.open(imgfp2).resize(
                                                                (64, 64),
                                                                Image.Resampling.NEAREST,
                                                            ),
                                                            (ci, 0),
                                                        )

                                            di_imgs_stream = io.BytesIO()
                                            di_imgs.save(di_imgs_stream, "WEBP")
                                            file2 = discord.File(
                                                io.BytesIO(di_imgs_stream.getvalue()),
                                                filename=f"{id}_loot.webp",
                                            )
                                            files.append(file2)
                                            embed.add_field(
                                                name="ドロップアイテム",
                                                value="",
                                                inline=False,
                                            )
                                            embed.set_image(url=f"attachment://{id}_loot.webp")

                                        embed.set_thumbnail(url=f"attachment://{id}.webp")

                                        typename_jp = "アイテム" if is_item else "ブロック"
                                        embed.set_author(name=typename_jp)

                                        await interaction.response.send_message(embed=embed, files=files)
                            return


async def setup(bot: commands.Bot):
    await bot.add_cog(CItem(bot))
