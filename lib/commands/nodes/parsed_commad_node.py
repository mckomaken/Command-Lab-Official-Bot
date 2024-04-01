from typing import Generic, TypeVar
from lib.commands.nodes import CommandNode
from lib.commands.range import StringRange


S = TypeVar("S")


class ParsedCommandNode(Generic[S]):
    def __init__(self, node: CommandNode[S], range: StringRange) -> None:
        self.node = node
        self.range = range

    def __str__(self) -> str:
        return f"{self.node}@{self.range}"
