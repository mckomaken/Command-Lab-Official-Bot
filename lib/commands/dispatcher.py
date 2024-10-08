import copy
import functools
import traceback
from typing import TypeVar

from lib.commands.builder.literal import LiteralArgumentBuilder
from lib.commands.builtin_exceptions import BUILT_IN_EXCEPTIONS
from lib.commands.context import CommandContextBuilder
from lib.commands.exceptions import CommandSyntaxException
from lib.commands.nodes import CommandNode
from lib.commands.nodes.literal import LiteralCommandNode
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
DEBUG = True


class CommandDispatcher:
    root: RootCommandNode

    def __init__(self) -> None:
        self.root = RootCommandNode()

    async def getCompletionSuggestions(self, parse: ParseResults[S], cursor: int = None) -> Suggestions:
        if cursor is None:
            cursor = parse.getReader().getTotalLength()

        context = parse.getContext()

        nodeBeforeCursor = context.findSuggestionContext(cursor)
        parent = nodeBeforeCursor.parent
        start = min(nodeBeforeCursor.startPos, cursor)

        fullInput = parse.getReader().getString()
        truncatedInput = fullInput[0:cursor]
        truncatedInputLowerCase = truncatedInput.lower()
        suggests: list[Suggestions] = []
        if DEBUG:
            print("DEBUG INFORMATION")
            print(f"In={fullInput} Cursor={cursor}")
            print(f"Context: ChildCount={len(context.nodes)}")

        for node in parent.getChildren():
            suggest = Suggestions.empty()
            try:
                suggest = await node.listSuggestions(
                    context.build(truncatedInput),
                    SuggestionsBuilder(truncatedInput, truncatedInputLowerCase, start),
                )
            except CommandSyntaxException as e:
                raise e
            suggests.append(suggest)

        suggestions: list[Suggestions] = []
        for suggest in suggests:
            suggestions.append(suggest)
        result = Suggestions.merge(fullInput, suggestions)

        return result

    def parse(self, command: StringReader, source: S):
        context = CommandContextBuilder(self, source, self.root, command.getCursor())
        return self.parseNodes(self.root, command, context)

    def parseNodes(
        self,
        node: CommandNode[S],
        originalReader: StringReader,
        contextSoFar: CommandContextBuilder[S],
    ) -> ParseResults:
        source: S = contextSoFar.getSource()
        errors: dict[CommandNode[S], CommandSyntaxException] = None
        potentials: list[ParseResults[S]] = None
        cursor = originalReader.getCursor()

        relevant = node.getRelevantNodes(originalReader)
        for child in relevant:
            if not child.canUse(source):
                continue

            context = copy.deepcopy(contextSoFar)
            reader = StringReader(originalReader)
            try:
                child.parse(reader, context)

                if reader.canRead():
                    if reader.peek() != ARGUMENT_SEPARATOR:
                        raise BUILT_IN_EXCEPTIONS.dispatcher_expected_argument_separator().createWithContext(reader)
            except CommandSyntaxException as ex:
                if errors is None:
                    errors = dict()
                errors[child] = ex
                reader.setCursor(cursor)
                continue

            context.withCommand(child.getCommand())
            if reader.canRead(2 if child.redirect is None else 1):
                reader.skip()
                if child.redirect is not None:
                    childContext = CommandContextBuilder[S](self, source, child.getRedirect(), reader.getCursor())
                    parse = self.parseNodes(child.redirect, reader, childContext)
                    context.withChild(parse.context)
                    return ParseResults(context, parse.getReader(), parse.getExceptions())
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
                def _cmp(a: ParseResults, b: ParseResults):
                    if not a.getReader().canRead() and b.getReader().canRead():
                        return -1
                    if a.getReader().canRead() and not b.getReader().canRead():
                        return 1
                    if len(a.getExceptions()) == 0 and len(b.getExceptions()) != 0:
                        return -1
                    if len(a.getExceptions()) != 0 and len(b.getExceptions()) == 0:
                        return 1
                    return 0

                potentials.sort(key=functools.cmp_to_key(_cmp))
            return potentials[0]

        return ParseResults(contextSoFar, originalReader, dict() if errors is None else errors)

    def register(self, command: LiteralArgumentBuilder[S]) -> LiteralCommandNode[S]:
        build = command.build()
        self.root.addChild(build)
        return build
