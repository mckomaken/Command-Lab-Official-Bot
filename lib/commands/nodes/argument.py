from typing import Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.context import CommandContext, CommandContextBuilder
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.nodes import CommandNode
from lib.commands.parsed_argument import ParsedArgument
from lib.commands.reader import StringReader
from lib.commands.redirect import RedirectModifier
from lib.commands.suggestions import SuggestionProvider, Suggestions, SuggestionsBuilder
from lib.commands.types import ArgumentType
from lib.commands.util.predicate import Predicate


class ArgumentCommandNode[S, T](CommandNode[S]):
    def __init__(
        self,
        name: str,
        type: ArgumentType[T],
        command: Command[S],
        requirement: Predicate[S],
        redirect: Self,
        modifier: RedirectModifier[S],
        forks: bool,
        customSuggestions: SuggestionProvider[S],
    ) -> None:
        super().__init__(command, requirement, redirect, modifier, forks)
        self.name = name
        self.type = type
        self.customSuggestions = customSuggestions
        self.children = dict()

    async def listSuggestions(self, context: CommandContext[S], builder: SuggestionsBuilder) -> Suggestions:
        if self.customSuggestions is None:
            return await self.type.listSuggestions(context, builder)
        else:
            return await self.customSuggestions.getSuggestions(context, builder)

    def parse(self, reader: StringReader, contextBuilder: CommandContextBuilder[S]):
        start = reader.getCursor()
        try:
            result = self.type.parse(reader)
        except CommandSyntaxException:
            raise
        parsed = ParsedArgument(start, reader.getCursor(), result)

        contextBuilder.withArgument(self.name, parsed)
        contextBuilder.withNode(self, parsed.range)

    def getName(self) -> str:
        return self.name

    def getCommand(self) -> Command[S]:
        return self.command

    def __str__(self) -> str:
        return f"argument[name={self.name},type={self.type}]"
