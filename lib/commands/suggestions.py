from typing import TYPE_CHECKING, Self

from lib.commands.util import classproperty

if TYPE_CHECKING:
    from lib.commands.context import CommandContext
    from lib.commands.nodes import CommandNode

from lib.commands.range import StringRange


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
            result += command[range.start : self.range.start]
        result += self.text
        if range.end > self.range.end:
            result += command[self.range.end : range.end]

        return Suggestion(range, result, self.tooltip)


class Suggestions:
    @classproperty
    def EMPTY(cls) -> Self:
        return cls(StringRange.at(0), [])

    def __init__(self, range: StringRange, suggestions: list[Suggestion]) -> None:
        self.range = range
        self.suggestions = suggestions

    def getList(self) -> list[Suggestion]:
        return self.suggestions

    def isEmpty(self) -> bool:
        return len(self.suggestions) == 0

    @staticmethod
    def empty() -> Self:
        return Suggestions.EMPTY

    @staticmethod
    def merge(command: str, input: list["Suggestions"]) -> "Suggestions":
        if len(input) == 0:
            return Suggestions.EMPTY
        elif len(input) == 1:
            return next(iter(input))

        texts: set[Suggestion] = set()
        for suggestion in input:
            for suggest in suggestion.getList():
                texts.add(suggest)

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

    def getInput(self) -> str:
        return self.input

    def getStart(self) -> int:
        return self.start

    def suggest(self, text: str, tooltip: str = None) -> Self:
        if text == self.remaining:
            return self

        self.result.append(
            Suggestion(StringRange.between(self.start, len(self.input)), text, tooltip)
        )
        return self

    def add(self, other: Self) -> Self:
        for v in other.result:
            self.result.append(v)
        return self

    def build(self):
        return Suggestions.create(self.input, self.result)

    async def build_async(self):
        return Suggestions.create(self.input, self.result)

    def createOffset(self, start: int):
        return SuggestionsBuilder(self.input, self.inputLowerCase, start)

    def __str__(self) -> str:
        return ",".join([v.text for v in self.result])

    def getRemaining(self):
        return self.remaining


class SuggestionProvider[S]:
    async def getSuggestions(
        self, context: "CommandContext[S]", builder: "SuggestionsBuilder"
    ):
        raise NotImplementedError()


class SuggestionContext[S]:
    parent: "CommandNode[S]"
    startPos: int

    def __init__(self, parent: "CommandNode[S]", startPos: int) -> None:
        self.parent = parent
        self.startPos = startPos

    def __str__(self) -> str:
        return f"SuggestionContext[parent={self.parent},startPos={self.startPos}]"
