import copy
from typing import Any, Coroutine, TypeVar

from lib.commands.context import CommandContextBuilder
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.nodes import CommandNode
from lib.commands.nodes.root import RootCommandNode
from lib.commands.parse_result import ParseResults
from lib.commands.reader import StringReader
from lib.commands.suggestions import Suggestions, SuggestionsBuilder

S = TypeVar("S")


USAGE_OPTIONAL_OPEN = "["
USAGE_OPTIONAL_CLOSE = "]"
USAGE_REQUIRED_OPEN = "("
USAGE_REQUIRED_CLOSE = ")"
USAGE_OR = "|"
ARGUMENT_SEPARATOR = " "


class CommandDispatcher:
    root: RootCommandNode

    def __init__(self) -> None:
        self.root = RootCommandNode()

    async def getCompletionSuggestions(self, parse: ParseResults[S], cursor: int = None) -> Suggestions:
        if cursor is None:
            cursor = parse.reader.getTotalLength()

        context = parse.getContext()

        nodeBeforeCursor = context.findSuggestionContext(cursor)
        parent = nodeBeforeCursor.parent
        start = min(nodeBeforeCursor.startPos, cursor)

        fullInput = parse.getReader().getString()
        truncatedInput = fullInput[0:cursor]
        truncatedInputLowerCase = truncatedInput.lower()
        futures: list[Coroutine[Any, Any, Suggestions]] = []

        for node in parent.children.values():
            future = Suggestions.empty()
            try:
                future = node.listSuggestions(context.build(truncatedInput), SuggestionsBuilder(truncatedInput, truncatedInputLowerCase, start))
            except CommandSyntaxException:
                pass
            futures.append(future)

        suggestions: list[Suggestions] = []
        for future in futures:
            suggestions.append(await future())
        result = Suggestions.merge(fullInput, suggestions)

        return result

    def parse(self, command: StringReader, source: S):
        context = CommandContextBuilder(self, source, self.root, command.getCursor())
        return self.parseNodes(self.root, command, context)

    def parseNodes(self, node: CommandNode[S], originalReader: StringReader, contextSoFar: CommandContextBuilder[S]) -> ParseResults:
        source: S = contextSoFar.get_source()
        errors: dict[CommandNode[S], CommandSyntaxException] = None
        potentials: list[ParseResults[S]] = None
        cursor = originalReader.getCursor()

        for child in node.getRelevantNodes(originalReader):
            if not child.canUse():
                continue

            context = copy.deepcopy(contextSoFar)
            reader = StringReader(originalReader)
            try:
                try:
                    child.parse(reader, context)
                except Exception as ex:
                    raise CommandSyntaxException.BUILT_IN_EXCEPTIONS.dispatcher_parse_expection().createWithContext(reader, str(ex))

                if reader.canRead():
                    if reader.peek() != ARGUMENT_SEPARATOR:
                        raise CommandSyntaxException.BUILT_IN_EXCEPTIONS.dispatcher_expected_argument_separator().createWithContext(reader)
            except CommandSyntaxException as ex:
                if errors is None:
                    errors = list()
                errors[child] = ex
                reader.setCursor(cursor)
                continue
            context.withCommand(child.command)
            if reader.canRead(2 if child.redirect is None else 1):
                reader.skip()
                if child.redirect is not None:
                    childContext = CommandContextBuilder[S](self, source, child.redirect, reader.getCursor())
                    parse: ParseResults[S] = self.parseNodes(child.redirect, reader, childContext)
                    context.withChild(parse.context)
                    return ParseResults[S](context, parse.reader, parse.exceptions)
                else:
                    parse = self.parseNodes(child, reader, context)
                    if potentials is None:
                        potentials = list()
                    potentials.append(parse)
            else:
                if potentials is None:
                    potentials = list()
                potentials.append(ParseResults[S](context, reader, dict()))

        if potentials is not None:
            if len(potentials) > 1:
                potentials.sort()
            return potentials[0]

        return ParseResults(contextSoFar, originalReader, dict() if errors is None else errors)
