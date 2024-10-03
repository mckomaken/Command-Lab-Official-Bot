import math
from typing import override
from lib.commands.builtin_exceptions import BUILT_IN_EXCEPTIONS
from lib.commands.context import CommandContext
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.reader import StringReader
from lib.commands.types import ArgumentType


class DoubleArgumentType(ArgumentType[float]):
    EXAMPLES = ["0", "1.2", ".5", "-1", "-.5", "-1234.56"]
    maximum: float
    minimum: float

    def __init__(self, minimun: float, maximun: float) -> None:
        self.minimum = minimun
        self.maximum = maximun

    def getDouble(self, context: CommandContext, name: str) -> float:
        return context.getArgument(name, float)

    def getMaximum(self):
        return self.maximum

    def getMinimum(self):
        return self.minimum

    def parse(self, reader: StringReader) -> float:
        start = reader.getCursor()
        result = reader.readDouble()
        if result < self.minimum:
            reader.setCursor(start)
            raise BUILT_IN_EXCEPTIONS.double_too_low().createWithContext(
                reader, result, self.minimum
            )
        if result > self.maximum:
            reader.setCursor(start)
            raise BUILT_IN_EXCEPTIONS.double_too_high().createWithContext(
                reader, result, self.maximum
            )

        return result

    def getExamples(self) -> list[str]:
        return self.EXAMPLES


def double_minmax(min, max) -> DoubleArgumentType:
    return DoubleArgumentType(min, max)


@override
def double_min(min) -> DoubleArgumentType:
    return double_minmax(min, math.inf)


@override
def double() -> DoubleArgumentType:
    return double_min(-math.inf, math.inf)
