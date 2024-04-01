
from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

from lib.commands.parsed_argument import ParsedArgument
from lib.commands.range import StringRange

if TYPE_CHECKING:
    from lib.commands import Command
    from lib.commands.nodes import CommandNode
    from lib.commands.nodes.parsed_commad_node import ParsedCommandNode
    from lib.commands.redirect import RedirectModifier


S = TypeVar("S")


class CommandContext(Generic[S]):
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


class CommandContextBuilder(Generic[S]):
    pass
