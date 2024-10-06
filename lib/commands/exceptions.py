from typing import TYPE_CHECKING, Callable, Optional


if TYPE_CHECKING:
    from lib.commands.reader import StringReader

from lib.commands.text import Text


class CommandSyntaxException(Exception):
    CONTEXT_AMOUNT = 50

    def __init__(self, exc_type, message: Text, str_input: Optional[str] = None, cursor: int = -1):
        super().__init__(message)
        self.type = exc_type
        self.message = message
        self.input = str_input
        self.cursor = cursor

    def get_message(self):
        message = self.message.getString()
        context = self.getContext()
        if context is not None:
            message += f" at position {self.cursor}: {context}"
        return message

    def getRawMessage(self) -> Text:
        return self.message

    def getContext(self):
        if self.input is None or self.cursor < 0:
            return None

        builder = ""
        cursor = min(len(self.input), self.cursor)
        if cursor > self.CONTEXT_AMOUNT:
            builder += "..."

        builder += self.input[max(0, self.cursor - self.CONTEXT_AMOUNT) : cursor]
        builder += "<--[HERE]"

        return builder

    def getType(self):
        return self.type

    def getInput(self):
        return self.input

    def getCursor(self):
        return self.cursor


class SimpleCommandExceptionType:
    def __init__(self, message: Text):
        self.message = message

    def create(self):
        return CommandSyntaxException(self, self.message)

    def createWithContext(self, reader: "StringReader"):
        return CommandSyntaxException(self, self.message, reader.getString(), reader.getCursor())

    def __str__(self):
        return self.message.getString()


class DynamicCommandExceptionType:
    def __init__(self, function: Callable[..., str]):
        self.function = function

    def create(self, *args):
        return CommandSyntaxException(self, self.function(*args))

    def createWithContext(self, reader: "StringReader", *args):
        return CommandSyntaxException(self, self.function(*args), reader.getString(), reader.getCursor())


class LiteralMessage:
    def __init__(self, string: str):
        self.string = string

    def getString(self):
        return self.string

    def __str__(self):
        return self.string
