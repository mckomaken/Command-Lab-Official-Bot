
from typing import Self, TypeVar

from lib.commands.argument_type import ArgumentType
from lib.commands.builder.argument import ArgumentBuilder
from lib.commands.nodes.argument import ArgumentCommandNode
from lib.commands.suggestions import SuggestionProvider


S = TypeVar("S")
T = TypeVar("T")


class RequiredArgumentBuilder(ArgumentBuilder[S, "RequiredArgumentBuilder[T]"]):
    name: str
    type: ArgumentType[T]
    suggestionsProvider: SuggestionProvider[S]

    def __init__(self, name: str, type: ArgumentType[T]):
        self.name = name
        self.type = type

    def suggests(self, provider: SuggestionProvider[S]) -> Self[S, T]:
        self.suggestionsProvider = provider
        return self

    def getSuggestionsProvider(self) -> SuggestionProvider[S]:
        return self.suggestionsProvider

    def getThis(self) -> Self:
        return self

    def getType(self) -> ArgumentType[T]:
        return self.type

    def getName(self) -> str:
        return self.name

    def build(self) -> Self:
        result = ArgumentCommandNode(
            self.getName(), self.getType(), self.getCommand(),
            self.getRequirement(), self.getRedirect(), self.getRedirectModifier(),
            self.isFork(), self.getSuggestionsProvider()
        )

        for argument in self.getArguments():
            result.addChild(argument)

        return result


def argument(name: str, type: ArgumentType[T]):
    return RequiredArgumentBuilder(name, type)
