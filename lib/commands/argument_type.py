import math
import re
import nbtlib
from enum import Enum
from typing import Any, Generic, TypeVar, overload

from lib.commands.context import CommandContext
from lib.commands.exceptions import (CommandSyntaxException,
                                     DynamicCommandExceptionType,
                                     SimpleCommandExceptionType)
from lib.commands.reader import StringReader
from lib.commands.selector import Selector
from lib.commands.source import ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.util import BlockPos, Vec2f, Vec3d
from schemas.data import DataPaths, Items

T = TypeVar("T")
S = TypeVar("S")


INCOMPLETE_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.incomplete"))
INVALID_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.invalid"))
MIXED_COORDINATE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.pos.mixed"))

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


E = TypeVar("E", Enum)

INVALID_ENUM_EXCEPTION = DynamicCommandExceptionType(lambda opt: Text.stringifiedTranslatable("argument.enum.invalid", [opt]))


class Angle:
    def __init__(self, angle: float, relative: bool) -> None:
        self.angle = angle
        self.relative = relative

    def get_angle(self, source: ServerCommandSource):
        return math.degrees(self.angle + source.get_rotation().y if self.relative else self.angle)


MISSING_COORDINATE = SimpleCommandExceptionType(Text.translatable("argument.pos.missing.double"))
MISSING_BLOCK_POSITION = SimpleCommandExceptionType(Text.translatable("argument.pos.missing.int"))


class CoordinateArgument:
    TILDE = "~"
    relative: bool
    value: float

    def __init__(self, relative: bool, value: float) -> None:
        self.relative = relative
        self.value = value

    def toAbsoluteCoordinate(self, offset: float):
        return self.value + offset if self.relative else self.value

    @staticmethod
    @overload
    def parse(reader: StringReader, centerIntegers: bool):
        if reader.canRead() and reader.peek() == '^':
            raise MIXED_COORDINATE_EXCEPTION.createWithContext(reader)
        elif not reader.canRead():
            raise MISSING_COORDINATE.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            i = reader.getCursor()
            d = reader.readDouble() if reader.canRead() and reader.peek() != ' ' else 0.0
            string = reader.getString()[i:reader.getCursor()]
            if bl and string == "":
                return CoordinateArgument(True, 0.0)
            else:
                if "." not in string and not bl and centerIntegers:
                    d += 0.5

                return CoordinateArgument(bl, d)

    @staticmethod
    @overload
    def parse(reader: StringReader):
        if reader.canRead() and reader.peek() == '^':
            raise MIXED_COORDINATE_EXCEPTION.createWithContext(reader)
        elif not reader.canRead():
            raise MISSING_BLOCK_POSITION.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            d = 0.0
            if reader.canRead() and reader.peek() != ' ':
                d = reader.readDouble() if bl else reader.read_int()

            return CoordinateArgument(bl, d)

    @staticmethod
    def isRelative(reader: StringReader):
        if reader.peek() == '~':
            bl = True
            reader.skip()
        else:
            bl = False

        return bl



class DoubleArgumentType(ArgumentType[bool]):
    EXAMPLES = ["0", "1.2", ".5", "-1", "-.5", "-1234.56"]
    minimum: float
    maximum: float

    def __init__(self, minimum: float, maximum: float) -> None:
        self.maximum = maximum
        self.minimum = minimum

    @staticmethod
    def double():
        return DoubleArgumentType()

    @staticmethod
    def get_double(context: CommandContext[Any], name: str):
        return context.getArgument(name, bool)

    def parse(self, reader: StringReader) -> bool:
        start = reader.getCursor()
        result = reader.readDouble()
        if result < self.minimum:
            reader.setCursor(start)
            raise CommandSyntaxException.BUILT_IN_EXCEPTIONS.double_too_low().createWithContext(reader)
        if result > self.maximum:
            reader.setCursor(start)
            raise CommandSyntaxException.BUILT_IN_EXCEPTIONS.double_too_high().createWithContext(reader)
        return result

    def get_examples(self) -> list[str]:
        return self.EXAMPLES


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


class EnumArgumentType(Generic[E], ArgumentType[Enum]):
    def parse(self, reader: StringReader) -> E:
        if isinstance(E, Enum[E]):
            string = reader.readUnquotedString()
            return E[string]

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        for e in list(E):
            builder.suggest(e)



class NbtArgumentType:
    def parse(self, reader: StringReader):
        nbt = nbtlib.parse_nbt(reader.read())

        return nbt

    def list_suggestions(self, builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def get_examples(self):
        return []


class ItemArgumentType:
    def parse(self, reader: StringReader):
        start = reader.getCursor()
        while reader.canRead() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start:reader.cursor]

        return d

    def list_suggestions(self, builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def get_examples(self):
        result = []
        with open("./minecraft_data/data/dataPaths.json") as fp:
            dataPath = DataPaths.model_validate_json(fp.read())
            with open("./minecraft_data/data/" + dataPath.pc[latest_version].items + "/items.json") as fp2:
                items = Items.model_validate_json(fp2.read())
                for item in items.root:
                    result.append(f"minecraft:{item.name}")
        return result


class EntityAnchor:
    pass


INVALID_ANCHOR_EXCEPTIONS = DynamicCommandExceptionType(lambda opt: Text.stringifiedTranslatable("argument.anchor.invalid", [opt]))


class EntityAnchorArgumentType(ArgumentType[EntityAnchor]):
    def parse(self, reader: StringReader) -> EntityAnchor:
        return

    @staticmethod
    def entity_anchor(self):
        return EntityAnchorArgumentType()

    @staticmethod
    def get_entity_anchor(self, context: CommandContext[ServerCommandSource], name: str):
        return context.getArgument(name, EntityAnchor)
