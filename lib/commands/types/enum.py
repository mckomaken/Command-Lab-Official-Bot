from enum import Enum
from typing import Generic, TypeVar

from lib.commands.context import CommandContext
from lib.commands.exceptions import DynamicCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.types import ArgumentType

E = TypeVar("E", Enum)

INVALID_ENUM_EXCEPTION = DynamicCommandExceptionType(
    lambda opt: Text.stringifiedTranslatable("argument.enum.invalid", [opt])
)

class EnumArgumentType(Generic[E], ArgumentType[Enum]):
    def parse(self, reader: StringReader) -> E:
        if isinstance(E, Enum[E]):
            string = reader.readUnquotedString()
            return E[string]

    def listSuggestions(self, context: CommandContext, builder: SuggestionsBuilder):
        for e in list(E):
            builder.suggest(e)