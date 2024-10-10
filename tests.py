import copy

import pytest

from lib.commands import loader
from lib.commands.dispatcher import CommandDispatcher
from lib.commands.entity import Entity, EntityType
from lib.commands.output import CommandOutput
from lib.commands.reader import StringReader
from lib.commands.server import MinecraftServer
from lib.commands.source import ServerCommandSource
from lib.commands.util import Vec2f
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.world import ServerWorld, World


@pytest.mark.asyncio
async def test_1():
    await loader.init()


@pytest.mark.asyncio
async def test_2():
    dispatcher = CommandDispatcher()
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

    dispatcher.parse(StringReader("give @s stone"), copy.deepcopy(source))
    dispatcher.parse(StringReader("clear @a"), copy.deepcopy(source))
    dispatcher.parse(StringReader(""), copy.deepcopy(source))
    dispatcher.parse(StringReader(""), copy.deepcopy(source))
