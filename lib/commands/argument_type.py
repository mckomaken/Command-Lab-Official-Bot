import math
from enum import Enum
from typing import Any, Generic, TypeVar, overload

from lib.commands.context import CommandContext
from lib.commands.exceptions import (
    CommandSyntaxException,
    DynamicCommandExceptionType,
    SimpleCommandExceptionType,
)
from lib.commands.reader import StringReader
from lib.commands.selector import Selector
from lib.commands.source import ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.util import BlockPos, Vec2f, Vec3d
from schemas.data import DataPaths, Items

T = TypeVar("T")
S = TypeVar("S")


INCOMPLETE_ANGLE_EXCEPTION = SimpleCommandExceptionType(
    Text.translatable("argument.angle.incomplete")
)
INVALID_ANGLE_EXCEPTION = SimpleCommandExceptionType(
    Text.translatable("argument.angle.invalid")
)

latest_version = "1.21.1"


class PosArgument:
    def toAbsolutePos(self, source: ServerCommandSource) -> Vec3d:
        raise NotImplementedError()

    def toAbsoluteRotation(self, source: ServerCommandSource) -> Vec2f:
        raise NotImplementedError()

    def toAbsoluteBlockPos(self, source: ServerCommandSource):
        return BlockPos.ofFloored(self.toAbsolutePos(source))

    def isXRelative(self):
        raise NotImplementedError()

    def isYRelative(self):
        raise NotImplementedError()

    def isZRelative(self):
        raise NotImplementedError()


class Vec3ArgumentType(ArgumentType[PosArgument]):
    def parse(self, reader: StringReader) -> PosArgument:
        return super().parse(reader)


class Angle:
    def __init__(self, angle: float, relative: bool) -> None:
        self.angle = angle
        self.relative = relative

    def get_angle(self, source: ServerCommandSource):
        return math.degrees(
            self.angle + source.get_rotation().y if self.relative else self.angle
        )


class AngleArgumentType(ArgumentType[Angle]):
    EXAMPLES = ["0", "~", "~-5"]

    def parse(self, reader: StringReader) -> Angle:
        if not reader.canRead():
            INCOMPLETE_ANGLE_EXCEPTION.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            f = reader.canRead() and reader.read_float() if reader.peek() != " " else 0
            if not math.isnan(f) and not math.isinf(f):
                return Angle(f, bl)
            else:
                raise INVALID_ANGLE_EXCEPTION.createWithContext(reader)

    def get_examples(self) -> list[str]:
        return self.EXAMPLES

    @staticmethod
    def angle():
        return AngleArgumentType()

    @staticmethod
    def get_angle(context: CommandContext[ServerCommandSource], name: str):
        return context.getArgument(name, Angle).get_angle(context.get_source())


class EntityAnchor:
    pass


INVALID_ANCHOR_EXCEPTIONS = DynamicCommandExceptionType(
    lambda opt: Text.stringifiedTranslatable("argument.anchor.invalid", [opt])
)


class EntityAnchorArgumentType(ArgumentType[EntityAnchor]):
    def parse(self, reader: StringReader) -> EntityAnchor:
        return

    @staticmethod
    def entity_anchor(self):
        return EntityAnchorArgumentType()

    @staticmethod
    def get_entity_anchor(
        self, context: CommandContext[ServerCommandSource], name: str
    ):
        return context.getArgument(name, EntityAnchor)
