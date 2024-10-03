from typing import Generic, TypeVar

from lib.commands.context import CommandContextBuilder
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.nodes import CommandNode
from lib.commands.reader import StringReader

S = TypeVar("S")


class ParseResults(Generic[S]):
    context: CommandContextBuilder[S]
    exceptions: dict[CommandNode[S], CommandSyntaxException]
    reader: StringReader

    def __init__(
        self,
        context: CommandContextBuilder[S],
        reader: StringReader,
        exceptions: dict[CommandNode[S], CommandSyntaxException],
    ):
        self.context = context
        self.reader = reader
        self.exceptions = exceptions

    @classmethod
    def fromContext(cls, context: CommandContextBuilder[S]):
        cls(context, StringReader(""), dict())

    def getContext(self):
        return self.context

    def getReader(self):
        return self.reader

    def getExceptions(self):
        return self.exceptions
