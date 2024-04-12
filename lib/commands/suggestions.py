from typing import TYPE_CHECKING, Generic, Self, TypeVar

if TYPE_CHECKING:
    from lib.commands.context import CommandContext
    from lib.commands.nodes import CommandNode
from lib.commands.range import StringRange

S = TypeVar("S")


class Suggestion:
    def __init__(self, range: StringRange, text: str, tooltip: str = None) -> None:
        self.range = range
        self.text = text
        self.tooltip = tooltip

    def expand(self, command: str, range: StringRange):
        if range == self.range:
            return self

        result = ""
        if range.start < self.range.start:
            result += command[range.start:self.range.start]
        result += self.text
        if range.end > self.range.end:
            result += command[self.range.end:range.end]

        return Suggestion(range, result, self.tooltip)


class Suggestions:
    @staticmethod
    @property
    def EMPTY():
        return Suggestions(StringRange.at(0), [])

    def __init__(self, range: StringRange, suggestions: list[Suggestion]) -> None:
        self.range = range
        self.suggestions = suggestions

    def get_list(self) -> list[Suggestion]:
        return self.suggestions

    def is_empty(self) -> bool:
        return len(self.suggestions) == 0

    @staticmethod
    def empty():
        async def _empty():
            return Suggestions.EMPTY
        return _empty()

    @staticmethod
    def merge(command: str, input: list["Suggestions"]) -> "Suggestions":
        if len(input) == 0:
            return Suggestions.EMPTY
        elif len(input) == 1:
            return next(input)

        texts: set[Suggestion] = set()
        for suggestion in input:
            texts.add(suggestion.get_list())

        return Suggestions.create(command, texts)

    @staticmethod
    def create(command: str, suggestions: list[Suggestion]) -> "Suggestions":
        if len(suggestions) == 0:
            return Suggestions.EMPTY
        start = 2147483647
        end = -2147483648
        for suggestion in suggestions:
            start = min(suggestion.range.start, start)
            end = max(suggestion.range.end, end)

        range = StringRange(start, end)
        texts: set[Suggestion] = set()
        for suggestion in suggestions:
            texts.add(suggestion.expand(command, range))

        sorte = sorted(texts, key=lambda a: a.text.lower())
        return Suggestions(range, sorte)


class SuggestionsBuilder:
    def __init__(self, input: str, inputLowerCase: str = None, start: int = 0) -> None:
        if inputLowerCase is None:
            inputLowerCase = input.lower()
        self.input = input
        self.inputLowerCase = inputLowerCase
        self.start = start
        self.remaining = input[start:]
        self.remainingLowerCase = inputLowerCase[start:]
        self.result: list[Suggestion] = list()

    def suggest(self, text: str, tooltip: str = None) -> Self:
        if text == self.remaining:
            return self

        self.result.append(Suggestion(StringRange.between(self.start, len(self.input)), text, tooltip))
        return self

    def add(self, other: Self) -> Self:
        self.result.append(other.result)
        return self

    def build(self):
        return Suggestions.create(self.input, self.result)

    def build_async(self):
        async def _a():
            self.build()
        return _a()


class SuggestionProvider(Generic[S]):
    def getSuggestions(self, context: "CommandContext[S]", builder: "SuggestionsBuilder"):
        raise NotImplementedError()


class SuggestionContext(Generic[S]):
    parent: "CommandNode[S]"
    startPos: int

    def __init__(self, parent: "CommandNode[S]", startPos: int) -> None:
        self.parent = parent
        self.startPos = startPos
