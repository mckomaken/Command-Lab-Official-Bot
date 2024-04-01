from typing import Generic, TypeVar
from lib.commands import StringRange, CommandNode


S = TypeVar("S")


class ParsedCommandNode(Generic[S]):
    def __init__(self, node: CommandNode[S], range: StringRange) -> None:
        self.node = node
        self.range = range

    def __str__(self) -> str:
        return f"{self.node}@{self.range}"
