from lib.commands.exceptions import SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.text import Text
from lib.commands.types import ArgumentType
from lib.commands.util.math.vec3d import Vec3d

MISSING_COORDINATE = SimpleCommandExceptionType(Text.translatable("argument.pos.missing.double"))
MIXED_COORDINATE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.pos.mixed"))
MISSING_BLOCK_POSITION = SimpleCommandExceptionType(Text.translatable("argument.pos.missing.int"))


class CoordinateArgument(ArgumentType[Vec3d]):
    TILDE = "~"
    relative: bool
    value: float

    def __init__(self, relative: bool, value: float) -> None:
        self.relative = relative
        self.value = value

    def toAbsoluteCoordinate(self, offset: float):
        return self.value + offset if self.relative else self.value

    @staticmethod
    def parse(reader: StringReader, centerIntegers: bool = None):
        if reader.canRead() and reader.peek() == "^":
            raise MIXED_COORDINATE_EXCEPTION.createWithContext(reader)
        elif not reader.canRead():
            raise MISSING_COORDINATE.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            i = reader.getCursor()
            d = reader.readDouble() if reader.canRead() and reader.peek() != " " else 0.0
            string = reader.getString()[i : reader.getCursor()]
            if bl and string == "":
                return CoordinateArgument(True, 0.0)
            else:
                if "." not in string and not bl and centerIntegers:
                    d += 0.5

                return CoordinateArgument(bl, d)

    @staticmethod
    def parse(reader: StringReader):
        if reader.canRead() and reader.peek() == "^":
            raise MIXED_COORDINATE_EXCEPTION.createWithContext(reader)
        elif not reader.canRead():
            raise MISSING_BLOCK_POSITION.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            d = 0.0
            if reader.canRead() and reader.peek() != " ":
                d = reader.readDouble() if bl else reader.read_int()

            return CoordinateArgument(bl, d)

    @staticmethod
    def isRelative(reader: StringReader):
        if reader.peek() == "~":
            bl = True
            reader.skip()
        else:
            bl = False

        return bl
