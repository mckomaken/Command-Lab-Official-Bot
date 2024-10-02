from typing import Generic, TypeVar

from lib.commands.context import CommandContext
from lib.commands.nodes import CommandNode
from lib.commands.nodes.literal import LiteralCommandNode
from lib.commands.suggestions import Suggestions, SuggestionsBuilder

S = TypeVar("S")


class RootCommandNode(Generic[S], CommandNode[S]):
    def __init__(self) -> None:
        super().__init__(None, lambda _: None, None, lambda s: [s.source], False)
        self.children = dict()

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        return Suggestions.empty()

    def __str__(self) -> str:
        return ""

    def register(self, literal: "LiteralCommandNode[S]"):
        self.children[literal.literal] = literal
