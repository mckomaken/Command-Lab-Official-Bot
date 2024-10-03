from lib.commands.context import CommandContext
from lib.commands.reader import StringReader
from lib.commands.types import ArgumentType
from lib.commands.util import classproperty


class StringType:
    examples: list[str]

    def __init__(self, *examples: str):
        self.examples = examples

    def getExamples(self) -> list[str]:
        return self.examples

    @classproperty
    def SINGLE_WORD(cls):
        return cls("word", "words_with_underscores")

    @classproperty
    def QUOTABLE_PHRASE(cls):
        return cls('"quoted phrase"', "word", '""')

    @classproperty
    def GREEDY_PHRASE(cls):
        return cls("word", "words with spaces", '"and symbols"')


class StringArgumentType(ArgumentType[str]):
    type: StringType

    def __init__(self, type: StringType) -> None:
        self.type = type

    @staticmethod
    def word():
        return StringArgumentType(StringType.SINGLE_WORD)

    @staticmethod
    def string():
        return StringArgumentType(StringType.QUOTABLE_PHRASE)

    @staticmethod
    def greedyString():
        return StringArgumentType(StringType.GREEDY_PHRASE)

    def getString(context: CommandContext, name: str) -> str:
        return context.getArgument(name, str)

    def getType(self) -> StringType:
        return self.type

    def parse(self, reader: StringReader):
        if self.type == StringType.GREEDY_PHRASE:
            text = reader.getRemaining()
            reader.setCursor(reader.getTotalLength())
            return text
        elif type == StringType.SINGLE_WORD:
            return reader.readUnquotedString()
        else:
            return reader.readString()

    def getExamples(self):
        return self.type.getExamples()

    def escapeIfRequired(self, inpu: str):
        for c in inpu:
            if not StringReader.is_allowed_in_unquoted_string(c):
                return self.escape(inpu)

        return inpu

    def escape(self, inpu: str):
        result = '"'

        for c in inpu:
            if c == "\\" or c == '"':
                result += "\\"
            result += c

        result += '"'
        return result
