from typing import TYPE_CHECKING, Generic, Self, TypeVar

from lib.commands.context import CommandContext, CommandContextBuilder
from lib.commands.reader import StringReader
from lib.commands.redirect import RedirectModifier
from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.util.predicate import Predicate

if TYPE_CHECKING:
    from lib.commands import Command
    from lib.commands.nodes.argument import ArgumentCommandNode
    from lib.commands.nodes.literal import LiteralCommandNode


class CommandNode[S]():
    command: "Command[S]"
    children: dict[str, Self] = dict()
    literals: dict[str, "LiteralCommandNode[S]"] = dict()
    arguments: dict[str, "ArgumentCommandNode[S]"] = dict()
    requirement: Predicate[S]
    redirect: Self
    modifier: RedirectModifier[S]
    forks: bool

    def __init__(
        self,
        command: "Command[S]",
        requirement: Predicate[S],
        redirect: Self,
        modifier: RedirectModifier[S],
        forks: bool,
    ) -> None:
        self.children = dict()
        self.arguments = dict()
        self.literals = dict()
        self.command = command
        self.requirement = requirement
        self.redirect = redirect
        self.modifier = modifier
        self.forks = forks

    async def listSuggestions(self, context: CommandContext[S], builder: SuggestionsBuilder):
        raise NotImplementedError()

    def getRelevantNodes(self, input: StringReader) -> list["CommandNode[S]"]:
        if len(self.literals) > 0:
            cursor = input.getCursor()
            while input.canRead() and input.peek() != " ":
                input.skip()

            text = input.getString()[cursor : input.getCursor()]
            input.setCursor(cursor)
            literal = self.literals.get(text)
            if literal is not None:
                return [literal]
            else:
                return self.arguments.values()
        else:
            return self.arguments.values()

    def getName(self) -> str:
        raise NotImplementedError()

    def getCommand(self) -> "Command[S]":
        raise NotImplementedError()

    def getChildren(self) -> list["CommandNode[S]"]:
        return self.children.values()

    def getRedirect(self) -> RedirectModifier[S]:
        return self.redirect

    def addChild(self, node: "CommandNode[S]"):
        from lib.commands.nodes.argument import ArgumentCommandNode
        from lib.commands.nodes.literal import LiteralCommandNode
        from lib.commands.nodes.root import RootCommandNode

        if isinstance(node, RootCommandNode):
            raise ValueError("Cannot add a RootCommandNode as a child to any other CommandNode")

        child = self.children.get(node.getName())
        if child is not None:
            if node.getCommand() is not None:
                child.command = node.getCommand()
            for grandchild in node.getChildren():
                child.addChild(grandchild)
        else:
            self.children[node.getName()] = node
            if isinstance(node, LiteralCommandNode):
                self.literals[node.getName()] = node
            elif isinstance(node, ArgumentCommandNode):
                self.arguments[node.getName()] = node

    def canUse(self, source: S):
        # return self.requirement.test(source)
        return True

    def parse(self, reader: StringReader, contextBuilder: CommandContextBuilder):
        raise NotImplementedError()
