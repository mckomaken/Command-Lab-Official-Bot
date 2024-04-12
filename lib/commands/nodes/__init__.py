from typing import TYPE_CHECKING, Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.context import CommandContext
from lib.commands.reader import StringReader
from lib.commands.redirect import RedirectModifier
from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.util.predicate import Predicate

if TYPE_CHECKING:
    from lib.commands.nodes.argument import ArgumentCommandNode
    from lib.commands.nodes.literal import LiteralCommandNode


S = TypeVar("S")


class CommandNode(Generic[S]):
    command: Command[S]
    children: dict[str, Self]
    literals: dict[str, "LiteralCommandNode[S]"] = dict()
    arguments: dict[str, "ArgumentCommandNode[S]"] = dict()
    requirement: Predicate[S]
    redirect: Self
    modifier: RedirectModifier[S]
    forks: bool

    def __init__(
        self,
        command: Command[S],
        requirement: Predicate[S],
        redirect: Self,
        modifier: RedirectModifier[S],
        forks: bool
    ) -> None:
        self.command = command
        self.requirement = requirement
        self.redirect = redirect
        self.modifier = modifier
        self.forks = forks

    def list_suggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        raise NotImplementedError()

    def getRelevantNodes(self, input: StringReader) -> list["CommandNode[S]"]:
        if len(self.literals) > 0:
            cursor = input.get_cursor()
            while input.can_read() and input.peek() != ' ':
                input.skip()

            text = input.get_string()[cursor:input.get_cursor()]
            input.set_cursor(cursor)
            literal = self.literals.get(text)
            if literal is not None:
                return [literal]
            else:
                return self.arguments.values()
        else:
            return self.arguments.values()

    def can_use(self):
        return True
