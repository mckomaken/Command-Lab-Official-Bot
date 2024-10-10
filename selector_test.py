import asyncio
import json
import math
import os
import traceback
from typing import Optional

import aiofiles
import colorama
import readchar
import tqdm

from cogs.ccommand import BaseParser
from lib.commands.builder.literal import LiteralArgumentBuilder, literal
from lib.commands.builder.required_argument import argument
from lib.commands.dispatcher import CommandDispatcher
from lib.commands.entity import Entity, EntityType
from lib.commands.nodes import CommandNode
from lib.commands.output import CommandOutput
from lib.commands.reader import StringReader
from lib.commands.schemas.data import (
    ArgumentParser,
    DataPaths,
    EntityArgumentModifier,
    parse_command,
)
from lib.commands.server import MinecraftServer
from lib.commands.source import ServerCommandSource
from lib.commands.types.boolean import BoolArgumentType
from lib.commands.types.double import DoubleArgumentType
from lib.commands.types.entity import EntityArgumentType
from lib.commands.types.integer import IntegerArgumentType
from lib.commands.types.item import ItemArgumentType
from lib.commands.types.nbt import NbtArgumentType
from lib.commands.types.string import StringArgumentType
from lib.commands.util import Vec2f
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.world import ServerWorld, World

colorama.init()
colorama.just_fix_windows_console()


parsers = {}
dispatcher = CommandDispatcher()


async def load():
    global parsers, dispatcher

    async with aiofiles.open(
        "./minecraft_data/data/dataPaths.json", mode="rb"
    ) as datap:
        cmds_path = (
            DataPaths.model_validate_json(await datap.read()).pc["1.20.4"].commands
        )

    async with aiofiles.open(
        "./minecraft_data/data/" + cmds_path + "/commands.json", mode="rb"
    ) as fp:
        raw = json.loads(await fp.read())
        cmds: list = raw["root"]["children"]
        _parsers: list = raw["parsers"]

    for c in _parsers:
        p = ArgumentParser.model_validate(c)

        def _parse(reader: StringReader):
            pass

        parsers[p.parser] = BaseParser(_parse, p.examples)

    async def _rescusive(
        builder: Optional[LiteralArgumentBuilder], _cmd: dict
    ) -> LiteralArgumentBuilder:
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

    progress = tqdm.tqdm(total=len(cmds))
    for cmd in cmds:
        data = await _rescusive(None, cmd)
        dispatcher.register(data)
        progress.update(1)


async def tree():
    global dispatcher

    async def _resc(root: CommandNode, depth=0):
        print(f"{"-" * depth * 2}> {root.getName()}")
        for child in root.children.values():
            await _resc(child, depth + 1)

    for c in dispatcher.root.children.values():
        await _resc(c)


async def main():
    await load()
    await tree()

    data = ""
    while True:
        d = readchar.readchar()
        if ord(d) == 0x0008:
            data = data[0 : len(data) - 1]
        elif ord(d) == 0x000A or ord(d) == 0x000D:
            data = ""
        else:
            data += d

        os.system("cls")
        print(data)

        if data == "exit":
            print("Exit.")
            return

        if data == "":
            return

        r = StringReader(data.lstrip())

        try:
            parsed = dispatcher.parse(
                r,
                ServerCommandSource(
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
                ),
            )
        except Exception as e:
            traceback.print_exception(e)

        if len(parsed.getExceptions().values()) >= 1:
            for e in parsed.getExceptions().values():
                print(colorama.Fore.RED + e.getMessage() + colorama.Fore.RESET)
        else:
            print(f"{colorama.Fore.GREEN}エラーなし{colorama.Fore.RESET}")

        opts = await dispatcher.getCompletionSuggestions(parsed, None)
        for a in opts.getList():
            print(
                f"{colorama.Fore.LIGHTBLACK_EX}{' ' * len(data)}{a.text}{' ' * (30 - len(a.text))}{a.tooltip}{colorama.Fore.RESET}"
            )


if __name__ == "__main__":
    asyncio.run(main())
