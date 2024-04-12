from enum import Enum
import math
from typing import Any, Generic, TypeVar, overload


from lib.commands.context import CommandContext
from lib.commands.reader import StringReader
from lib.commands.source import ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.exceptions import CommandSyntaxException, DynamicCommandExceptionType, SimpleCommandExceptionType
from lib.commands.text import Text
from lib.commands.util import BlockPos, Vec2f, Vec3d

T = TypeVar("T")
S = TypeVar("S")


INCOMPLETE_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.incomplete"))
INVALID_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.invalid"))
MIXED_COORDINATE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.pos.mixed"))


class ArgumentType(Generic[T]):
    def parse(self, reader: StringReader) -> T:
        raise NotImplementedError()

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        return Suggestions.empty()

    def get_examples(self) -> list[str]:
        return []


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
        if reader.can_read() and reader.peek() == '^':
            raise MIXED_COORDINATE_EXCEPTION.create_with_context(reader)
        elif not reader.can_read():
            raise MISSING_COORDINATE.create_with_context(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            i = reader.get_cursor()
            d = reader.read_double() if reader.can_read() and reader.peek() != ' ' else 0.0
            string = reader.get_string()[i:reader.get_cursor()]
            if bl and string == "":
                return CoordinateArgument(True, 0.0)
            else:
                if "." not in string and not bl and centerIntegers:
                    d += 0.5

                return CoordinateArgument(bl, d)

    @staticmethod
    @overload
    def parse(reader: StringReader):
        if reader.can_read() and reader.peek() == '^':
            raise MIXED_COORDINATE_EXCEPTION.create_with_context(reader)
        elif not reader.can_read():
            raise MISSING_BLOCK_POSITION.create_with_context(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            d = 0.0
            if reader.can_read() and reader.peek() != ' ':
                d = reader.read_double() if bl else reader.read_int()

            return CoordinateArgument(bl, d)

    @staticmethod
    def isRelative(reader: StringReader):
        if reader.peek() == '~':
            bl = True
            reader.skip()
        else:
            bl = False

        return bl


class BoolArgumentType(ArgumentType[bool]):
    EXAMPLES = ["true", "false"]

    @staticmethod
    def boolean():
        return BoolArgumentType()

    @staticmethod
    def get_bool(context: CommandContext[Any], name: str):
        return context.get_argument(name, bool)

    def parse(self, reader: StringReader) -> bool:
        return reader.read_boolean()

    def get_examples(self) -> list[str]:
        return self.EXAMPLES


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
        return context.get_argument(name, bool)

    def parse(self, reader: StringReader) -> bool:
        start = reader.get_cursor()
        result = reader.read_double()
        if result < self.minimum:
            reader.set_cursor(start)
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.double_too_low().create_with_context(reader)
        if result > self.maximum:
            reader.set_cursor(start)
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.double_too_high().create_with_context(reader)
        return result

    def get_examples(self) -> list[str]:
        return self.EXAMPLES


class AngleArgumentType(ArgumentType[Angle]):
    EXAMPLES = ["0", "~", "~-5"]

    def parse(self, reader: StringReader) -> Angle:
        if not reader.can_read():
            INCOMPLETE_ANGLE_EXCEPTION.create_with_context(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            f = reader.can_read() and reader.read_float() if reader.peek() != " " else 0
            if not math.isnan(f) and not math.isinf(f):
                return Angle(f, bl)
            else:
                raise INVALID_ANGLE_EXCEPTION.create_with_context(reader)

    def get_examples(self) -> list[str]:
        return self.EXAMPLES

    @staticmethod
    def angle():
        return AngleArgumentType()

    @staticmethod
    def get_angle(context: CommandContext[ServerCommandSource], name: str):
        return context.get_argument(name, Angle).get_angle(context.get_source())


class EnumArgumentType(Generic[E], ArgumentType[Enum]):
    def parse(self, reader: StringReader) -> E:
        if isinstance(E, Enum[E]):
            string = reader.read_unquoted_string()
            return E[string]

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        for e in list(E):
            builder.suggest(e)


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
        return context.get_argument(name, EntityAnchor)
