import json
import math
from typing import Optional

import aiofiles
import colorama

from cogs.ccommand import BaseParser
from lib.commands.builder.literal import LiteralArgumentBuilder, literal
from lib.commands.builder.required_argument import argument
from lib.commands.dispatcher import CommandDispatcher
from lib.commands.reader import StringReader
from lib.commands.schemas.data import ArgumentParser, DataPaths, EntityArgumentModifier, parse_command
from lib.commands.types.boolean import BoolArgumentType
from lib.commands.types.double import DoubleArgumentType
from lib.commands.types.entity import EntityArgumentType
from lib.commands.types.integer import IntegerArgumentType
from lib.commands.types.item import ItemArgumentType
from lib.commands.types.nbt import NbtArgumentType
from lib.commands.types.string import StringArgumentType

colorama.init()
colorama.just_fix_windows_console()


parsers = {}
dispatcher = CommandDispatcher()

async def init():
    global parsers, dispatcher

    async with aiofiles.open("./minecraft_data/data/dataPaths.json", mode="rb") as datap:
        cmds_path = DataPaths.model_validate_json(await datap.read()).pc["1.20.4"].commands

    async with aiofiles.open("./minecraft_data/data/" + cmds_path + "/commands.json", mode="rb") as fp:
        raw = json.loads(await fp.read())
        cmds: list = raw["root"]["children"]
        _parsers: list = raw["parsers"]

    for c in _parsers:
        p = ArgumentParser.model_validate(c)

        def _parse(reader: StringReader):
            pass

        parsers[p.parser] = BaseParser(_parse, p.examples)

    async def _rescusive(builder: Optional[LiteralArgumentBuilder], _cmd: dict) -> LiteralArgumentBuilder:
        cmd = await parse_command(_cmd)

        if cmd.type == "literal":
            b = literal(cmd.name)
        elif cmd.type == "argument":
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
                modifier = EntityArgumentModifier.model_validate(cmdp.modifier)
                if modifier.type == "entities":
                    if modifier.amount == "single":
                        parser = EntityArgumentType.entity()
                    else:
                        parser = EntityArgumentType.entities()
                else:
                    if modifier.amount == "single":
                        parser = EntityArgumentType.player()
                    else:
                        parser = EntityArgumentType.players()
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
        else:
            raise Exception()

        for _cmd_c in cmd.children:
            await _rescusive(b, _cmd_c)

        for _cmd_r in cmd.redirects:
            b.redirect(_cmd_r)

        if builder is None:
            return b
        else:
            return builder.then(b)

    for cmd in cmds:
        data = await _rescusive(None, cmd)
        dispatcher.register(data)