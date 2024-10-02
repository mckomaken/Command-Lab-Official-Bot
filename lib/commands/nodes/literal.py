from typing import Any, Coroutine, Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.context import CommandContextBuilder
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.nodes import CommandNode
from lib.commands.range import StringRange
from lib.commands.reader import StringReader
from lib.commands.redirect import RedirectModifier
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.util.predicate import Predicate

S = TypeVar("S")


class LiteralCommandNode(Generic[S], CommandNode[S]):
    literal: str
    literalLowerCase: str

    def __init__(
        self,
        literal: str,
        command: Command[S],
        requirement: Predicate[S],
        redirect: Self,
        modifier: RedirectModifier[S],
        forks: bool
    ) -> None:
        super().__init__(command, requirement, redirect, modifier, forks)
        self.literal = literal
        self.literalLowerCase = literal.lower()

    def parse(self, reader: StringReader, builder: CommandContextBuilder[S] = None):
        start = reader.getCursor()
        end = self._parse()

        if end > -1:
            builder.withChild(self, StringRange(start, end))
        else:
            raise CommandSyntaxException.BUILT_IN_EXCEPTIONS

    def _parse(self, reader: StringReader) -> int:
        start: int = reader.getCursor()
        if reader.canRead(len(self.literal)):
            end = start + len(self.literal)
            if reader.getString()[start:end] == self.literal:
                reader.setCursor(end)
                if not reader.canRead() or reader.peek() == ' ':
                    return end
                else:
                    reader.setCursor(start)
        return -1

    def listSuggestions(self, builder: SuggestionsBuilder) -> Coroutine[Any, Any, Suggestions]:
        if self.literalLowerCase.startswith(builder.remaining.lower()):
            return builder.suggest(self.literal, "").build_async()
        else:
            return Suggestions.empty()

    def is_valid_input(self, input: str):
        return self._parse(StringReader(input)) > -1
