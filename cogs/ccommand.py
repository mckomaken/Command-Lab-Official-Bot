import json
import math
import os
from datetime import datetime
import traceback
from typing import Any, Optional

import aiofiles
import discord
from lib.commands.dispatcher import CommandDispatcher
from lib.commands.entity import Entity, EntityType
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.builder.literal import LiteralArgumentBuilder, literal
from lib.commands.builder.required_argument import argument
from lib.commands.output import CommandOutput
from lib.commands.reader import StringReader
from lib.commands.server import MinecraftServer
from lib.commands.source import ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from discord import Embed, app_commands
from discord.ext import commands
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from tqdm import tqdm

from lib.commands.types.boolean import BoolArgumentType
from lib.commands.types.double import DoubleArgumentType
from lib.commands.types.integer import IntegerArgumentType
from lib.commands.types.item import ItemArgumentType
from lib.commands.types.nbt import NbtArgumentType
from lib.commands.types.selector import SelectorArgumentType
from lib.commands.types.string import StringArgumentType
from lib.commands.util import Vec2f
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.world import ServerWorld, World
from schemas.data import (
    ArgumentCommandEntry,
    ArgumentParser,
    CommandEntry,
    DataPaths,
    LiteralCommandEntry,
    parse_command,
)
from utils.util import create_codeblock, create_embed


class BaseParser:
    def __init__(self, parse, examples: list[str]):
        self._parse = parse
        self.examples = examples

    def parse(self, reader: StringReader):
        self._parse(reader)

    def list_suggestions(self, builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def get_examples(self):
        return self.examples


class Identifier:
    namespace: str
    path: str

    def __init__(self, id: str) -> None:
        self.namespace = id.split(":", maxsplit=1)[0]
        self.path = id.split(":", maxsplit=1)[1]

    @classmethod
    def __get_validators__(cls):
        yield cls.check

    @classmethod
    def check(cls, cont: str):
        if ":" in cont:
            raise TypeError("Invalid Identifier")

        return cont

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


class CCommandInfoButtons(discord.ui.View):
    def __init__(self, je: Optional[Embed] = None, be: Optional[Embed] = None):
        super().__init__(timeout=None)
        if je is None:
            self.je.disabled = True
        if be is None:
            self.be.disabled = True
        self.je_embed = je
        self.be_embed = be

    @discord.ui.button(label="JE")
    async def je(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.je_embed)

    @discord.ui.button(label="BE")
    async def be(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.be_embed)


class CCommandInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ccommand", description="コマンドの情報を表示します")
    async def ccommand(self, interaction: discord.Interaction, command: str):
        async with aiofiles.open(os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb") as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]
            if command not in data:
                await interaction.response.send_message(
                    embed=create_embed(title="エラー", description="コマンドが不明です")
                )
                return
            d = CommandEntry.model_validate(data[command])

        je_embed = None
        be_embed = None
        if d.ver.je is not None:
            je_embed = Embed(
                color=0xAA00BB,
                title=f"/{command}",
                description=d.desc,
                timestamp=datetime.now(),
            )
            je_embed.set_author(name="Java Edition")
            je_embed.add_field(
                name="使用法",
                value=create_codeblock("/" + d.options.je if d.options.je != "-" else f"/{command}"),
                inline=False,
            )
            je_embed.add_field(
                name="例",
                value=create_codeblock(d.exmp.je if d.exmp.je != "-" else f"/{command}"),
                inline=False,
            )

        if d.ver.be is not None:
            be_embed = Embed(
                color=0xAA00BB,
                title=f"/{command}",
                description=d.desc,
                timestamp=datetime.now(),
            )
            be_embed.set_author(name="Bedrock Edition")
            be_embed.add_field(
                name="使用法",
                value=create_codeblock("/" + d.options.be if d.options.be != "-" else f"/{command}"),
                inline=False,
            )
            be_embed.add_field(
                name="例",
                value=create_codeblock(d.exmp.be if d.exmp.be != "-" else f"/{command}"),
                inline=False,
            )

        view = None
        if d.is_diff:
            view = CCommandInfoButtons(je_embed, be_embed)

        await interaction.response.send_message(embed=(je_embed or be_embed), view=view)

    @ccommand.autocomplete("command")
    async def ccommand_autocomplete(self, interaction: discord.Interaction, current: str):
        async with aiofiles.open(os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb") as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]

            return [app_commands.Choice(name=k, value=k) for k in data.keys() if k.startswith(current)][:25]

    @app_commands.command(name="crun", description="コマンドの実行結果をシミュレーションします")
    async def crun(self, interaction: discord.Interaction, command: str):
        result = self.dispatcher.execute(command)
        embed = discord.Embed(title="コマンド実行", description=create_codeblock(command))
        embed.add_field(name="結果", value=create_codeblock(result))

        await interaction.response.send_message(embed=embed)

    @crun.autocomplete("command")
    async def crun_autocomplete(self, interaction: discord.Interaction, current: str):
        try:
            source = ServerCommandSource(
                CommandOutput.DUMMY,
                Vec3d(0, 0, 0),
                Vec2f(0, 0),
                ServerWorld(),
                1,
                "akpc_0504",
                "ap12",
                MinecraftServer(),
                Entity(EntityType.PLAYER, World()),
                False,
                print,
            )
            parsed = self.dispatcher.parse(StringReader(current), source)
            opts = self.dispatcher.getCompletionSuggestions(parsed, None)
            result = list()

            for node in opts.get_list():
                try:
                    result.append(node.text)
                except CommandSyntaxException as e:
                    return [app_commands.Choice(name=e, value=e)]
            return [app_commands.Choice(name=f"{n} ", value=f"{n} ") for n in result][:25]
        except Exception as e:
            traceback.print_exception(e)

    async def cog_load(self):
        async with aiofiles.open("./minecraft_data/data/dataPaths.json", mode="rb") as datap:
            cmds_path = DataPaths.model_validate_json(await datap.read()).pc["1.20.4"].commands

        async with aiofiles.open("./minecraft_data/data/" + cmds_path + "/commands.json", mode="rb") as fp:
            raw = json.loads(await fp.read())
            cmds: list = raw["root"]["children"]
            parsers: list = raw["parsers"]

        self.parsers = {}

        for c in parsers:
            p = ArgumentParser.model_validate(c)

            def _parse(reader: StringReader):
                pass

            self.parsers[p.parser] = BaseParser(_parse, p.examples)

        self.dispatcher = CommandDispatcher()

        async def _rescusive(builder: Optional[LiteralArgumentBuilder], _cmd: dict) -> LiteralArgumentBuilder:
            cmd = await parse_command(_cmd)
            if isinstance(cmd, LiteralCommandEntry):
                b = literal(cmd.name)
            if isinstance(cmd, ArgumentCommandEntry):
                cmdp = cmd.parser
                if cmdp.parser == "brigadier:integer" or cmdp.parser == "minecraft:time":
                    minimum = -2147483648
                    maximum = 2147483647
                    if cmdp.modifier is not None:
                        if "min" in cmdp.modifier:
                            minimum = cmdp.modifier["min"]
                        if "max" in cmdp.modifier:
                            maximum = cmdp.modifier["max"]
                    parser = IntegerArgumentType.integer_minmax(minimum, maximum)

                elif cmdp.parser == "brigadier:string":
                    if cmdp.modifier is not None:
                        parser = StringArgumentType.string()
                    else:
                        if "type" in cmdp.modifier:
                            if cmdp.modifier["type"] == "greedy":
                                parser = StringArgumentType.greedyString()
                            elif cmdp.modifier["type"] == "word":
                                parser = StringArgumentType.word()

                elif cmdp.parser == "brigadier:double" or cmdp.parser == "brigadier:float":
                    minimum = -math.inf
                    maximum = math.inf
                    if cmdp.modifier is not None:
                        if "min" in cmdp.modifier:
                            minimum = cmdp.modifier["min"]
                        if "max" in cmdp.modifier:
                            maximum = cmdp.modifier["max"]

                    parser = DoubleArgumentType(minimum, maximum)

                elif cmdp.parser == "minecraft:entity":
                    parser = SelectorArgumentType()
                elif cmdp.parser == "brigadier:bool":
                    parser = BoolArgumentType.boolean()
                elif cmdp.parser == "minecraft:nbt_compound_tag":
                    parser = NbtArgumentType()
                elif cmdp.parser == "minecraft:item_stack":
                    parser = ItemArgumentType()
                else:
                    print(f"Argument {cmd.name} {cmdp.parser} load failed!")
                    return

                b = argument(cmd.name, parser)

            for _cmd_c in cmd.children:
                await _rescusive(b, _cmd_c)

            for _cmd_r in cmd.redirects:
                b.redirect(_cmd_r)

            if builder is None:
                return b
            else:
                return builder.then(b)

        progress = tqdm(total=len(cmds))
        for cmd in cmds:
            data = await _rescusive(None, cmd)
            self.dispatcher.register(data)
            progress.update(1)


async def setup(bot: commands.Bot):
    await bot.add_cog(CCommandInfo(bot))
