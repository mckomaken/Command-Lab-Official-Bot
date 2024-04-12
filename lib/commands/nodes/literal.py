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
        start = reader.get_cursor()
        end = self._parse()

        if end > -1:
            builder.with_node(self, StringRange(start, end))
        else:
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS

    def _parse(self, reader: StringReader) -> int:
        start: int = reader.get_cursor()
        if reader.can_read(len(self.literal)):
            end = start + len(self.literal)
            if reader.get_string()[start:end] == self.literal:
                reader.set_cursor(end)
                if not reader.can_read() or reader.peek() == ' ':
                    return end
                else:
                    reader.set_cursor(start)
        return -1

    def list_suggestions(self, builder: SuggestionsBuilder) -> Coroutine[Any, Any, Suggestions]:
        if self.literalLowerCase.startswith(builder.remaining.lower()):
            return builder.suggest(self.literal, "").build_async()
        else:
            return Suggestions.empty()

    def is_valid_input(self, input: str):
        return self._parse(StringReader(input)) > -1
