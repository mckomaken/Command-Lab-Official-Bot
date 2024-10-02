

from typing import Generic, TypeVar

from lib.commands.context import CommandContext
from lib.commands.reader import StringReader
from lib.commands.suggestions import Suggestions, SuggestionsBuilder

T = TypeVar("T")
S = TypeVar("S")


class ArgumentType(Generic[T]):
    def parse(self, reader: StringReader) -> T:
        raise NotImplementedError()

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def getExamples(self) -> list[str]:
        return []
