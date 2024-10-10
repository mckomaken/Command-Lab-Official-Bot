from typing import TYPE_CHECKING, Any, Self, Type

from lib.commands.parsed_argument import ParsedArgument
from lib.commands.range import StringRange

if TYPE_CHECKING:
    from lib.commands.dispatcher import CommandDispatcher
    from lib.commands.nodes.parsed_commad_node import ParsedCommandNode
    from lib.commands import Command
    from lib.commands.nodes import CommandNode
    from lib.commands.redirect import RedirectModifier

from lib.commands.suggestions import SuggestionContext


class CommandContext[S]:
    source: S
    input: str
    command: "Command[S]"
    arguments: dict[str, ParsedArgument[S, Any]]
    rootNode: "CommandNode[S]"
    nodes: list["ParsedCommandNode[S]"]
    range: StringRange
    child: Self
    modifier: "RedirectModifier[S]"
    forks: bool

    def __init__(
        self,
        source: S,
        input: str,
        arguments: dict[str, ParsedArgument[S, Any]],
        command: "Command[S]",
        rootNode: "CommandNode[S]",
        nodes: list["ParsedCommandNode[S]"],
        range: StringRange,
        child: "CommandContext[S]",
        modifier: "RedirectModifier[S]",
        forks: bool,
    ) -> None:
        self.source = source
        self.input = input
        self.arguments = arguments
        self.command = command
        self.rootNode = rootNode
        self.nodes = nodes
        self.range = range
        self.child = child
        self.modifier = modifier
        self.forks = forks

    def getArgument[V](self, name: str, clazz: Type[V]):
        argument: ParsedArgument[S, V] = self.arguments.get(name)
        if argument is None:
            raise ValueError("No such argument '" + name + "' exists on this command")

        result = argument.result
        if r := clazz(result):
            return r
        else:
            raise ValueError(
                "Argument '"
                + name
                + "' is defined as "
                + str(V)
                + ", not "
                + str(clazz)
            )

    def getSource(self):
        return self.source


class CommandContextBuilder[S]:
    arguments: dict[str, ParsedArgument[S, Any]] = dict()
    rootNode: "CommandNode[S]"
    nodes: list["ParsedCommandNode[S]"] = []
    dispatcher: "CommandDispatcher[S]"
    source: S
    command: "Command[S]"
    child: Self
    range: StringRange
    modifier: "RedirectModifier[S]" = None
    forks: bool

    def __init__(
        self,
        dispatcher: "CommandDispatcher[S]",
        source: S,
        rootNode: "CommandNode[S]",
        start: int,
    ):
        self.arguments = dict()
        self.nodes = list()
        self.rootNode = rootNode
        self.dispatcher = dispatcher
        self.source = source
        self.range = StringRange.at(start)
        self.child = None
        self.modifier = None
        self.command = None
        self.forks = False

    def withSource(self, source: S) -> Self:
        self.source = source
        return self

    def getSource(self) -> S:
        return self.source

    def findSuggestionContext(self, cursor: int) -> "SuggestionContext[S]":
        if self.range.start <= cursor:
            if self.range.end < cursor:
                if self.child is not None:
                    return self.child.findSuggestionContext(cursor)
                elif len(self.nodes) != 0:
                    last = self.nodes[-1]
                    return SuggestionContext(last.node, last.range.end + 1)
                else:
                    return SuggestionContext(self.rootNode, self.range.start)
            else:
                prev = self.rootNode
                for node in self.nodes:
                    nodeRange = node.range
                    if nodeRange.start <= cursor and cursor <= nodeRange.end:
                        return SuggestionContext(prev, nodeRange.start)
                    prev = node.node
                if prev is None:
                    raise ValueError("Can't find node before cursor")
                return SuggestionContext(prev, self.range.start)
        raise ValueError("Can't find node before cursor")

    def build(self, input: str):
        return CommandContext(
            self.source,
            input,
            self.arguments,
            self.command,
            self.rootNode,
            self.nodes,
            self.range,
            None if self.child is None else self.child.build(input),
            self.modifier,
            self.forks,
        )

    def __str__(self) -> str:
        return f"CommandContextBuilder[range={self.range},nodes={len(self.nodes)}]"

    def withChild(self, child: "CommandContextBuilder[S]"):
        self.child = child
        return self

    def withCommand(self, command: "Command[S]"):
        self.command = command
        return self

    def withNode(self, node: "CommandNode[S]", range: StringRange):
        from lib.commands.nodes.parsed_commad_node import ParsedCommandNode

        self.nodes.append(ParsedCommandNode(node, range))
        self.range = StringRange.encompassing(self.range, range)
        self.modifier = node.modifier
        self.forks = node.forks
        return self

    def withArgument(self, name: str, argument: ParsedArgument[S, Any]):
        self.arguments[name] = argument
        return self
