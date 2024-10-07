from typing import Callable, TypeVar

from lib.commands.entity import Entity
from lib.commands.output import CommandOutput
from lib.commands.server import MinecraftServer
from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.util import Identifier, Vec2f
from lib.commands.util.consumer import Consumer, ReturnValueConsumer
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.world import ServerWorld

T = TypeVar("T")


def common_prefix(a: str, b: str):
    if not a:
        return ""
    for i, c in enumerate(a):
        if c != b[i]:
            return a[:i]
    return a


def should_suggest(remaining: str, candinate: str):
    i = 0
    while candinate.startswith(remaining, i):
        i += 1
        i = candinate.find(chr(95), i)
        if i < 0:
            return False

    return True


class CommandSource:
    @classmethod
    def suggest_identifiers(cls, candinates: list[Identifier], builder: SuggestionsBuilder, prefix: str):
        string = builder.remaining.lower()
        cls.for_each_matching(candinates, string, lambda id: id, lambda id: builder.suggest(str(id)))

        return builder.build()

    @classmethod
    def for_each_matching(
        cls,
        candinates: list[T],
        remaining: str,
        identitfier: Callable[[T], Identifier],
        action: Consumer[T],
    ):
        bl = remaining.find(chr(58)) > -1
        var5 = iter(candinates)

        while True:
            obj = next(var5, None)
            while obj:
                obj = next(obj, None)
                identifier2 = identitfier(obj)
                if bl:
                    string = str(identifier2)
                    if should_suggest(remaining, string):
                        action.accept(obj)

                elif (
                    should_suggest(remaining, identifier2.get_namespace())
                    or identifier2.get_namespace() == "minecraft"
                    and should_suggest(remaining, identifier2.get_path())
                ):
                    action.accept(obj)

    def getPlayerNames():
        raise NotImplementedError()


class ServerCommandSource(CommandSource):
    def __init__(
        self,
        output: CommandOutput,
        pos: Vec3d,
        rot: Vec2f,
        world: ServerWorld,
        level: int,
        name: str,
        displayName: Text,
        server: MinecraftServer,
        entity: Entity,
        silent: bool,
        resultStorer: ReturnValueConsumer,
    ) -> None:
        self.output = output
        self.pos = pos
        self.rot = rot
        self.world = world
        self.level = level
        self.name = name
        self.displayName = displayName
        self.server = server
        self.entity = entity
        self.silent = silent
        self.resultStorer = resultStorer
        super().__init__()

    def getServer(self):
        return self.server

    def getPosition(self):
        return self.pos

    def getEntity(self):
        return self.entity

    def getWorld(self):
        return self.world

    def getPlayerNames(self):
        return self.server.getPlayerNames()
