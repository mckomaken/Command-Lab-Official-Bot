from math import isfinite, isnan
from lib.commands.context import CommandContext
from lib.commands.exceptions import SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.source import ServerCommandSource
from lib.commands.text import Text
from lib.commands.types import ArgumentType
from lib.commands.types.coordinate import CoordinateArgument
from lib.commands.util.mathhelper import MathHelper


class Angle:
    def __init__(self, angle: float, relative: bool) -> None:
        self.angle = angle
        self.relative = relative

    def getAngle(self, source: ServerCommandSource):
        return MathHelper.wrapDegrees(self.angle + source.getRotation().y if self.relative else self.angle)


INCOMPLETE_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.incomplete"))
INVALID_ANGLE_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.angle.invalid"))


class AngleArgumentType(ArgumentType[Angle]):
    EXAMPLES = ["0", "~", "~-5"]

    @staticmethod
    def angle():
        return AngleArgumentType()

    @staticmethod
    def getAngle(context: CommandContext[ServerCommandSource], name: str):
        return context.getArgument(name, Angle).getAngle(context.getSource())

    def parse(self, reader: StringReader) -> Angle:
        if not reader.canRead():
            raise INCOMPLETE_ANGLE_EXCEPTION.createWithContext(reader)
        else:
            bl = CoordinateArgument.isRelative(reader)
            f = reader.read_float() if reader.canRead() and reader.peek() != " " else 0.0
            if not isnan(f) and not isfinite(f):
                return Angle(f, bl)
            else:
                raise INVALID_ANGLE_EXCEPTION.createWithContext(reader)

    def getExamples(self) -> list[str]:
        return self.EXAMPLES
