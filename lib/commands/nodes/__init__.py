from typing import TYPE_CHECKING, Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.redirect import RedirectModifier
from lib.commands.util.predicate import Predicate

if TYPE_CHECKING:
    from lib.commands.nodes.argument import ArgumentCommandNode
    from lib.commands.nodes.literal import LiteralCommandNode


S = TypeVar("S")


class CommandNode(Generic[S]):
    command: Command[S]
    children: dict[str, Self[S]]
    literals: dict[str, "LiteralCommandNode[S]"] = dict()
    arguments: dict[str, "ArgumentCommandNode[S]"] = dict()
    requirement: Predicate[S]
    redirect: Self[S]
    modifier: RedirectModifier[S]
    forks: bool

    def __init__(
        self,
        command: Command[S],
        requirement: Predicate[S],
        redirect: Self[S],
        modifier: RedirectModifier[S],
        forks: bool
    ) -> None:
        self.command = command
        self.requirement = requirement
        self.redirect = redirect
        self.modifier = modifier
        self.forks = forks
