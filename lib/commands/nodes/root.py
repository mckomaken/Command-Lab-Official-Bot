from typing import TypeVar

from lib.commands.context import CommandContext, CommandContextBuilder
from lib.commands.nodes import CommandNode
from lib.commands.nodes.literal import LiteralCommandNode
from lib.commands.reader import StringReader
from lib.commands.suggestions import Suggestions, SuggestionsBuilder

S = TypeVar("S")


class RootCommandNode(CommandNode[S]):
    def __init__(self) -> None:
        super().__init__(None, lambda _: True, None, lambda s: [s.getSource()], False)

    def getName(self) -> str:
        return ""

    def parse(self, reader: StringReader, contextBuilder: CommandContextBuilder):
        pass

    def isValidInput(self, input: str):
        return False

    async def listSuggestions(self, context: CommandContext[S], builder: SuggestionsBuilder) -> Suggestions:
        return Suggestions.empty()

    def __str__(self) -> str:
        return "<root>"

    def register(self, literal: "LiteralCommandNode[S]"):
        self.children[literal.literal] = literal
