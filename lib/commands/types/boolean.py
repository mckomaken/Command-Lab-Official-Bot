from typing import Any

from lib.commands.context import CommandContext
from lib.commands.reader import StringReader
from lib.commands.types import ArgumentType


class BoolArgumentType(ArgumentType[bool]):
    EXAMPLES = ["true", "false"]

    @staticmethod
    def boolean():
        return BoolArgumentType()

    @staticmethod
    def get_bool(context: CommandContext[Any], name: str):
        return context.getArgument(name, bool)

    def parse(self, reader: StringReader) -> bool:
        return reader.readBoolean()

    def getExamples(self) -> list[str]:
        return self.EXAMPLES
