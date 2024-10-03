import string
from typing import Self, Union

from lib.commands.builtin_exceptions import BUILT_IN_EXCEPTIONS
from lib.commands.exceptions import CommandSyntaxException

SYNTAX_ESCAPE = "\\"
SYNTAX_DOUBLE_QUOTE = '"'
SYNTAX_SINGLE_QUOTE = "'"


class StringReader:
    string: str
    cursor: int

    def __init__(self, other: Union[Self, str]):
        if isinstance(other, str):
            self.string = other
            self.cursor = 0
        else:
            self.string = other.string
            self.cursor = other.cursor

    def getString(self):
        return self.string

    def setCursor(self, cursor: int):
        self.cursor = cursor

    def getRemainingLength(self):
        return len(self.string) - self.cursor

    def getTotalLength(self):
        return len(self.string)

    def getCursor(self):
        return self.cursor

    def getRead(self):
        return self.string[0 : self.cursor]

    def getRemaining(self):
        return self.string[self.cursor :]

    def canRead(self, length: int = 1):
        return self.cursor + length <= len(self.string)

    def peek(self, offset: int = 0):
        return self.string[self.cursor + offset]

    def read(self):
        s = self.string[self.cursor]
        self.cursor += 1
        return s

    def skip(self):
        self.cursor += 1

    @staticmethod
    def is_allowed_number(c: str):
        return c >= "0" and c <= "9" or c == "." or c == "-"

    @staticmethod
    def is_quoted_string_start(c: str):
        return c == SYNTAX_DOUBLE_QUOTE or c == SYNTAX_SINGLE_QUOTE

    def skipWhitespace(self):
        while self.canRead() and self.peek == " ":
            self.skip()

    def read_int(self):
        start = self.cursor
        while self.canRead() and self.is_allowed_number(self.peek()):
            self.skip()

        number = string[start : self.cursor]
        if number == " ":
            raise BUILT_IN_EXCEPTIONS.reader_expected_int().createWithContext(self)

        try:
            return int(number)
        except Exception:
            self.cursor = start
            raise BUILT_IN_EXCEPTIONS.reader_invalid_int().createWithContext(
                self, number
            )

    def read_long(self) -> int:
        return self.read_int()

    def read_float(self) -> float:
        start = self.cursor
        while self.canRead() and self.is_allowed_number(self.peek()):
            self.skip()

        number = self.string[start : self.cursor]
        if number == "":
            raise BUILT_IN_EXCEPTIONS.reader_expected_double().createWithContext(self)

        try:
            return float(number)
        except Exception:
            self.cursor = start
            raise BUILT_IN_EXCEPTIONS.reader_invalid_double().createWithContext(
                self, number
            )

    def readDouble(self):
        return self.read_float()

    @staticmethod
    def is_allowed_in_unquoted_string(c: str):
        return (
            c >= "0"
            and c <= "9"
            or c >= "A"
            and c <= "Z"
            or c >= "a"
            and c <= "z"
            or c == "_"
            or c == "-"
            or c == "."
            or c == "+"
        )

    def readUnquotedString(self):
        start = self.cursor
        while self.canRead() and self.is_allowed_in_unquoted_string(self.peek()):
            self.skip()

        return self.string[start : self.cursor]

    def readQuotedString(self):
        if not self.canRead():
            return ""

        next = self.peek()
        if self.is_quoted_string_start(next):
            raise BUILT_IN_EXCEPTIONS.reader_expected_start_of_quote().createWithContext(
                self
            )

        self.skip()
        return self.readStringUntil(next)

    def readStringUntil(self, terminator: str):
        result = ""
        escaped = False
        while self.canRead():
            c = self.read()
            if escaped:
                if c == terminator or c == SYNTAX_ESCAPE:
                    result += c
                    escaped = False
                else:
                    self.setCursor(self.getCursor() - 1)
                    raise BUILT_IN_EXCEPTIONS.reader_invalid_escape().createWithContext(
                        self, str(c)
                    )

            elif c == SYNTAX_ESCAPE:
                escaped = True
            elif c == terminator:
                return result
            else:
                result += c

        raise BUILT_IN_EXCEPTIONS.reader_expected_end_of_quote().createWithContext(self)

    def readString(self):
        if not self.canRead():
            return ""

        next = self.peek()
        if self.is_quoted_string_start(next):
            self.skip()
            return self.readStringUntil(next)

        return self.readUnquotedString()

    def readBoolean(self):
        start = self.cursor
        value = self.readString()
        if value == "":
            raise BUILT_IN_EXCEPTIONS.reader_expected_bool().createWithContext(self)

        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            self.cursor = start
            raise BUILT_IN_EXCEPTIONS.reader_invalid_bool().createWithContext(
                self, value
            )

    def expect(self, c):
        if not self.canRead() or self.peek() != c:
            raise BUILT_IN_EXCEPTIONS.reader_expected_symbol().createWithContext(
                self, str(c)
            )

        self.skip()
