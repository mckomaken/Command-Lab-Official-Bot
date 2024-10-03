import math
from typing import Self
from lib.commands.builtin_exceptions import BUILT_IN_EXCEPTIONS
from lib.commands.context import CommandContext
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.reader import StringReader
from lib.commands.types import ArgumentType


class IntegerArgumentType(ArgumentType[int]):
    EXAMPLES = ["0", "1.2", ".5", "-1", "-.5", "-1234.56"]
    maximum: int
    minimum: int

    def __init__(self, minimun: int, maximun: int) -> None:
        self.minimum = minimun
        self.maximum = maximun

    def getDouble(self, context: CommandContext, name: str) -> int:
        return context.getArgument(name, int)

    def getMaximum(self):
        return self.maximum

    def getMinimum(self):
        return self.minimum

    def parse(self, reader: StringReader) -> int:
        start = reader.getCursor()
        result = reader.readDouble()
        if (result < self.minimum):
            reader.setCursor(start)
            raise BUILT_IN_EXCEPTIONS.integer_too_low() \
                .createWithContext(reader, result, self.minimum)
        if (result > self.maximum):
            reader.setCursor(start)
            raise BUILT_IN_EXCEPTIONS.integer_too_high() \
                .createWithContext(reader, result, self.maximum)

        return result

    def getExamples(self) -> list[str]:
        return self.EXAMPLES

    @classmethod
    def integer_minmax(cls, min, max) -> Self:
        return cls(min, max)

    @classmethod
    def integer_min(cls, min) -> Self:
        return cls.integer_minmax(min, math.inf)

    @classmethod
    def integer(cls) -> Self:
        return cls.integer_min(-math.inf, math.inf)
