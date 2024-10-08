from typing import Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.builder import literal
from lib.commands.builtin_exceptions import BUILT_IN_EXCEPTIONS
from lib.commands.context import CommandContext, CommandContextBuilder
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
        forks: bool,
    ) -> None:
        super().__init__(command, requirement, redirect, modifier, forks)
        self.literal = literal
        self.literalLowerCase = literal.lower()

    def parse(self, reader: StringReader, builder: CommandContextBuilder[S] = None):
        start = reader.getCursor()
        end = self._parse(reader)

        if end > -1:
            builder.withNode(self, StringRange(start, end))
            return

        raise BUILT_IN_EXCEPTIONS.literal_incorrect().createWithContext(reader, self.literal)

    def _parse(self, reader: StringReader) -> int:
        start: int = reader.getCursor()
        if reader.canRead(len(self.literal)):
            end = start + len(self.literal)
            if reader.getString()[start:end] == self.literal:
                reader.setCursor(end)
                if not reader.canRead() or reader.peek() == " ":
                    return end
                else:
                    reader.setCursor(start)
        return -1

    async def listSuggestions(self, context: CommandContext[S], builder: SuggestionsBuilder) -> Suggestions:
        if self.literalLowerCase.startswith(builder.remaining.lower()):
            return await builder.suggest(self.literal).build_async()
        else:
            return Suggestions.empty()

    def isValidInput(self, input: str):
        return self._parse(StringReader(input)) > -1

    def getName(self) -> str:
        return self.literal

    def getCommand(self) -> Command[S]:
        return self.command

    def __str__(self) -> str:
        return f"literal[{self.literal}]"
