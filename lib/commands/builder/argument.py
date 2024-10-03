from typing import Any, Generic, Self, TypeVar

from lib.commands import Command
from lib.commands.nodes import CommandNode
from lib.commands.nodes.root import RootCommandNode
from lib.commands.redirect import RedirectModifier
from lib.commands.util.predicate import Predicate


S = TypeVar("S")
T = TypeVar("T")


class ArgumentBuilder(Generic[S, T]):
    arguments: RootCommandNode[S]
    command: Command[S]
    requirement: Predicate[S]
    target: CommandNode[S]
    modifier: RedirectModifier[S]
    forks: bool

    def __init__(self) -> None:
        self.arguments = RootCommandNode[S]()
        self.command = None
        self.target = None
        self.requirement = Predicate(lambda _: True)
        self.modifier = None
        self.forks = False

    def getThis(self) -> Self:
        return self

    def then(self, argument: "ArgumentBuilder[S, Any]") -> T:
        if self.target is not None:
            raise ValueError("Cannot add children to a redirected node")
        self.arguments.addChild(argument.build())
        return self.getThis()

    def getArguments(self) -> list[CommandNode[S]]:
        return self.arguments.getChildren()

    def executes(self, command: Command[S]) -> T:
        self.command = command
        return self.getThis()

    def getCommand(self) -> Command[S]:
        return self.command

    def requires(self, requirement: Predicate[S]) -> T:
        self.requirement = requirement
        return self.getThis()

    def getRequirement(self) -> Predicate[S]:
        return self.requirement

    def forward(
        self, target: CommandNode[S], modifier: RedirectModifier[S], fork: bool
    ):
        if len(self.arguments.getChildren()) != 0:
            raise ValueError("Cannot forward a node with children")
        self.target = target
        self.modifier = modifier
        self.forks = fork

        return self.getThis()

    def redirect(self, target: CommandNode[S]) -> T:
        return self.forward(target, None, False)

    def fork(self, target: CommandNode[S], modifier: RedirectModifier[S]) -> T:
        return self.forward(target, modifier, True)

    def getRedirect(self) -> CommandNode[S]:
        return self.target

    def getRedirectModifier(self) -> RedirectModifier[S]:
        return self.modifier

    def isFork(self) -> bool:
        return self.forks

    def build(self) -> CommandNode[S]:
        raise NotImplementedError()
