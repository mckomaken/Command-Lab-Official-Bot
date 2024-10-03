from typing import TypeVar
from lib.commands.builder.argument import ArgumentBuilder
from lib.commands.nodes.literal import LiteralCommandNode


S = TypeVar("S")


class LiteralArgumentBuilder(ArgumentBuilder[S, "LiteralArgumentBuilder[S]"]):
    def __init__(self, literal):
        super().__init__()
        self.literal = literal

    def getThis(self):
        return self

    def getLiteral(self):
        return self.literal

    def build(self):
        result = LiteralCommandNode(
            self.getLiteral(),
            self.getCommand(),
            self.getRequirement(),
            self.getRedirect(),
            self.getRedirectModifier(),
            self.isFork(),
        )
        for argument in self.getArguments():
            result.addChild(argument)
        return result

    def __str__(self) -> str:
        return f"literal[{self.literal}]"


def literal(name):
    return LiteralArgumentBuilder(name)
