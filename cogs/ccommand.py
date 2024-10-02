import json
import math
import os
import re
from datetime import datetime
from typing import Any, Literal, Optional

import aiofiles
import discord
import nbtlib
from brigadier import CommandDispatcher, ParseResult, arguments
from brigadier.builder import LiteralArgumentBuilder, argument, literal
from brigadier.context import CommandContextBuilder, SuggestionContext
from brigadier.exceptions import CommandSyntaxException
from brigadier.parse_result import StringReader
from brigadier.suggestion import SuggestionsBuilder, empty_suggestion
from brigadier.tree import ArgumentCommandNode, LiteralCommandNode
from discord import Embed, app_commands
from discord.ext import commands
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from tqdm import tqdm

from config import config
from schemas.data import (ArgumentCommandEntry, ArgumentParser, CommandEntry,
                          DataPaths, Items, LiteralCommandEntry, parse_command)
from utils.util import create_codeblock, create_embed


class BaseParser():
    def __init__(self, parse, examples: list[str]):
        self._parse = parse
        self.examples = examples

    def parse(self, reader: StringReader):
        self._parse(reader)

    def list_suggestions(self, builder: SuggestionsBuilder):
        return empty_suggestion()

    def get_examples(self):
        return self.examples


class RangedNumber:
    min: int | float
    max: int | float
    original: str

    def __init__(self, cont: str) -> None:
        self.min = cont.split("..", maxsplit=1)[0] or -2147483648
        self.max = cont.split("..", maxsplit=1)[1] or 2147483647
        self.original = cont

    @classmethod
    def __get_validators__(cls):
        yield cls.check

    @classmethod
    def check(cls, cont: str):
        if ".." in cont:
            raise TypeError("Invalid range number")
        _min = cont.split("..", maxsplit=1)[0]
        _max = cont.split("..", maxsplit=1)[1]

        if not (_min.isdigit() or (_min.replace('.', '', 1).isdigit() and _min.count('.') < 2)):
            raise TypeError("Invalid minimum value of range number")

        if not (_max.isdigit() or (_max.replace('.', '', 1).isdigit() and _max.count('.') < 2)):
            raise TypeError("Invalid maximum value of range number")

        return cont

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


RangeNumberOrNumber = RangedNumber | float | int


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


class Selector(BaseModel):
    target: Literal["this", "all_entities", "all_players", "random_player", "nearest_player"]
    distance: Optional[RangeNumberOrNumber] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    dx: Optional[float] = None
    dy: Optional[float] = None
    dz: Optional[float] = None
    scores: Optional[dict[str, RangeNumberOrNumber]] = None
    tag: Optional[str] = None
    team: Optional[str] = None
    limit: Optional[int] = -1
    sort: Optional[Literal["nearest", "furthest", "random", "arbitrary"]] = None
    level: Optional[RangeNumberOrNumber] = None
    gamemode: Optional[Literal["survival", "adventure", "creative", "spectator"]] = None
    x_rotation: Optional[RangeNumberOrNumber] = None
    y_rotation: Optional[RangeNumberOrNumber] = None
    type: Optional[Identifier] = None
    nbt: Optional[dict] = None
    advancements: Optional[dict] = None
    predicate: Optional[Identifier] = None


SELECTOR_PATTERN = re.compile(
    r"(@e|@s|@r|@p|@a)\[((target|distance|x|y|z|dx|dy|dz|scores|tag|team|limit|sort|level|gamemode|x_rotation|y_rotation|type|nbt|advancements|predicate)=(.+?))*\]"
)


class SelectorArgumentType:
    def parse(self, reader: StringReader):
        start = reader.get_cursor()
        while reader.can_read() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start:reader.cursor]
        gps = SELECTOR_PATTERN.match(d)
        print(d)
        if gps is None:
            raise CommandSyntaxException(message="Selector Error")

        atX = gps.group(0)
        if atX == "@e":
            selector = Selector(target="all_entities")
        elif atX == "@p":
            selector = Selector(target="nearest_player")
        elif atX == "@a":
            selector = Selector(target="all_players")
        elif atX == "@r":
            selector = Selector(target="random_player")
        elif atX == "@s":
            selector = Selector(target="nearest_player")
        else:
            raise CommandSyntaxException(message="Selector Error")

        for gpIndex in range(2, len(gps.groups()) - 2, 2):
            key = gps.group(gpIndex)
            value = gps.group(gpIndex + 1)

            if key is None or value is None:
                raise CommandSyntaxException(message="Selector Error")

        return selector

    def list_suggestions(self, builder: SuggestionsBuilder):
        builder.add("@a")
        builder.add("@p")
        builder.add("@e")
        builder.add("@r")
        builder.add("@s")
        return builder.build()

    def get_examples(self):
        return ["@p", "@r", "@a", "@e", "@s"]


class NbtArgumentType:
    def parse(self, reader: StringReader):
        nbt = nbtlib.parse_nbt(reader.read())

        return nbt

    def list_suggestions(self, builder: SuggestionsBuilder):
        return empty_suggestion()

    def get_examples(self):
        return []


class ItemArgumentType:
    def parse(self, reader: StringReader):
        start = reader.get_cursor()
        while reader.can_read() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start:reader.cursor]

        return d

    def list_suggestions(self, builder: SuggestionsBuilder):
        return empty_suggestion()

    def get_examples(self):
        result = []
        with open("./minecraft_data/data/dataPaths.json") as fp:
            dataPath = DataPaths.model_validate_json(fp.read())
            with open("./minecraft_data/data/" + dataPath.pc[config.latest_version].items + "/items.json") as fp2:
                items = Items.model_validate_json(fp2.read())
                for item in items.root:
                    result.append(f"minecraft:{item.name}")
        return result


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
                value=create_codeblock(
                    "/" + d.options.je if d.options.je != "-" else f"/{command}"
                ),
                inline=False,
            )
            je_embed.add_field(
                name="例",
                value=create_codeblock(
                    d.exmp.je if d.exmp.je != "-" else f"/{command}"
                ),
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
                value=create_codeblock(
                    "/" + d.options.be if d.options.be != "-" else f"/{command}"
                ),
                inline=False,
            )
            be_embed.add_field(
                name="例",
                value=create_codeblock(
                    d.exmp.be if d.exmp.be != "-" else f"/{command}"
                ),
                inline=False,
            )

        view = None
        if d.is_diff:
            view = CCommandInfoButtons(je_embed, be_embed)

        await interaction.response.send_message(embed=(je_embed or be_embed), view=view)

    @ccommand.autocomplete("command")
    async def ccommand_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        async with aiofiles.open(os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb") as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]

            return [
                app_commands.Choice(name=k, value=k)
                for k in data.keys()
                if k.startswith(current)
            ][:25]

    @app_commands.command(
        name="crun",
        description="コマンドの実行結果をシミュレーションします"
    )
    async def crun(self, interaction: discord.Interaction, command: str):
        result = self.dispatcher.execute(command)
        embed = discord.Embed(
            title="コマンド実行",
            description=create_codeblock(command)
        )
        embed.add_field(name="結果", value=create_codeblock(result))

        await interaction.response.send_message(embed=embed)

    @crun.autocomplete("command")
    async def crun_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        parse: ParseResult = self.dispatcher.parse(current, {})
        cursor = len(current)
        context: CommandContextBuilder = parse.get_context()
        node_before_cursor: SuggestionContext = context.find_suggestion_context(cursor)
        parent: LiteralCommandNode = node_before_cursor.parent
        result: list[str] = []
        childrens: list[LiteralCommandNode | ArgumentCommandNode] = parent.get_children()
        print(current[node_before_cursor.start_pos:])

        for node in childrens:
            try:
                if isinstance(node, LiteralCommandNode):
                    result.append(node.get_name())
                if isinstance(node, ArgumentCommandNode):
                    for n in node.get_examples():
                        result.append(n)
            except CommandSyntaxException as e:
                return [
                    app_commands.Choice(name=e, value=e)
                ]
        return [
            app_commands.Choice(name=f"{n} ", value=f"{n} ") for n in result
        ][:25]

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
                    parser = arguments.integer_argument_type.integer(minimum, maximum)

                elif cmdp.parser == "brigadier:string":
                    if cmdp.modifier is not None:
                        parser = arguments.string_argument_type.string()
                    else:
                        if "type" in cmdp.modifier:
                            if cmdp.modifier["type"] == "greedy":
                                parser = arguments.string_argument_type.greedy_string()
                            elif cmdp.modifier["type"] == "word":
                                parser = arguments.string_argument_type.word()

                elif cmdp.parser == "brigadier:double" or cmdp.parser == "brigadier:float":
                    minimum = -math.inf
                    maximum = math.inf
                    if cmdp.modifier is not None:
                        if "min" in cmdp.modifier:
                            minimum = cmdp.modifier["min"]
                        if "max" in cmdp.modifier:
                            maximum = cmdp.modifier["max"]

                    parser = arguments.float_argument_type.float_type(minimum, maximum)

                elif cmdp.parser == "minecraft:entity":
                    parser = SelectorArgumentType()
                elif cmdp.parser == "brigadier:bool":
                    parser = arguments.BoolArgumentType()
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
                b.redirect(target=_cmd_r, modifier=None)

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
