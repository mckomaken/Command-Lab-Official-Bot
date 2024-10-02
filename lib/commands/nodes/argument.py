from typing import Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.argument_type import ArgumentType
from lib.commands.context import CommandContext
from lib.commands.nodes import CommandNode
from lib.commands.redirect import RedirectModifier
from lib.commands.suggestions import SuggestionProvider, SuggestionsBuilder
from lib.commands.util.predicate import Predicate

S = TypeVar("S")
T = TypeVar("T")


class ArgumentCommandNode(Generic[S, T], CommandNode[S]):
    def __init__(
        self,
        name: str,
        type: ArgumentType[T],
        command: Command[S],
        requirement: Predicate[S],
        redirect: Self,
        modifier: RedirectModifier[S],
        forks: bool,
        customSuggestions: SuggestionProvider[S]
    ) -> None:
        super().__init__(command, requirement, redirect, modifier, forks)
        self.name = name
        self.type = type
        self.customSuggestions = customSuggestions
        self.children = dict()

    def listSuggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        if self.customSuggestions is None:
            return self.type.list_suggestions(context, builder)
        else:
            return self.customSuggestions.getSuggestions(context, builder)
