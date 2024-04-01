from typing import Generic, TypeVar

from lib.commands.range import StringRange

T = TypeVar("T")
S = TypeVar("S")


class ParsedArgument(Generic[S, T]):
    range: StringRange
    result: T

    def __init__(self, start: int, end: int, result: T) -> None:
        self.range = StringRange(start, end)
        self.result = result
