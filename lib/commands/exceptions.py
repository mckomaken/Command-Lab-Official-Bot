from typing import Callable, Optional
from lib.commands.text import Text
from brigadier import StringReader


class CommandSyntaxException(Exception):
    CONTEXT_AMOUNT = 50

    def __init__(self, exc_type, message: Text, str_input: Optional[str] = None, cursor: int = -1):
        super().__init__(message)
        self.type = exc_type
        self.message = message
        self.input = str_input
        self.cursor = cursor

    def get_message(self):
        message = self.message.get_string()
        context = self.get_context()
        if context is not None:
            message += f" at position {self.cursor}: {context}"
        return message

    def get_raw_message(self) -> Text:
        return self.message

    def get_context(self):
        if self.input is None or self.cursor < 0:
            return None

        builder = ""
        cursor = min(len(self.input), self.cursor)
        if cursor > self.CONTEXT_AMOUNT:
            builder += "..."

        builder += self.input[max(0, self.cursor - self.CONTEXT_AMOUNT):cursor]
        builder += "<--[HERE]"

        return builder

    def get_type(self):
        return self.type

    def get_input(self):
        return self.input

    def get_cursor(self):
        return self.cursor


class SimpleCommandExceptionType:
    def __init__(self, message: Text):
        self.message = message

    def create(self):
        return CommandSyntaxException(self, self.message)

    def create_with_context(self, reader: StringReader):
        return CommandSyntaxException(self, self.message, reader.get_string(), reader.get_cursor())

    def __str__(self):
        return self.message.get_string()


class DynamicCommandExceptionType:
    def __init__(self, function: Callable[...]):
        self.function = function

    def create(self, *args):
        return CommandSyntaxException(self, self.function(*args))

    def create_with_context(self, reader: StringReader, *args):
        return CommandSyntaxException(self, self.function(*args), reader.get_string(), reader.get_cursor())
