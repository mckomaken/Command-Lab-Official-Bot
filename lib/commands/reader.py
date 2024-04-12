import string
from typing import Self, Union

from lib.commands.exceptions import CommandSyntaxException

SYNTAX_ESCAPE = '\\'
SYNTAX_DOUBLE_QUOTE = '"'
SYNTAX_SINGLE_QUOTE = '\''


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

    def get_string(self):
        return self.string

    def set_cursor(self, cursor: int):
        self.cursor = cursor

    def get_remaining_length(self):
        return len(self.string) - self.cursor

    def get_total_length(self):
        return len(self.string)

    def get_cursor(self):
        return self.cursor

    def get_read(self):
        return self.string[0:self.cursor]

    def get_remaining(self):
        return self.string[self.cursor:]

    def can_read(self, length: int = 1):
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
        return c >= '0' and c <= '9' or c == '.' or c == '-'

    @staticmethod
    def is_quoted_string_start(c: str):
        return c == SYNTAX_DOUBLE_QUOTE or c == SYNTAX_SINGLE_QUOTE

    def skipWhitespace(self):
        while self.can_read() and self.peek == " ":
            self.skip()

    def read_int(self):
        start = self.cursor
        while self.can_read() and self.is_allowed_number(self.peek()):
            self.skip()

        number = string[start:self.cursor]
        if number == " ":
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_int().create_with_context(self)

        try:
            return int(number)
        except Exception:
            self.cursor = start
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_invalid_int().create_with_context(self, number)

    def read_long(self) -> int:
        return self.read_int()

    def read_float(self) -> float:
        start = self.cursor
        while self.can_read() and self.is_allowed_number(self.peek()):
            self.skip()

        number = self.string[start:self.cursor]
        if number == "":
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_double().create_with_context(self)

        try:
            return float(number)
        except Exception:
            self.cursor = start
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_invalid_double().create_with_context(self, number)

    def read_double(self):
        return self.read_float()

    @staticmethod
    def is_allowed_in_unquoted_string(c: str):
        return c >= '0' and c <= '9' \
            or c >= 'A' and c <= 'Z' \
            or c >= 'a' and c <= 'z' \
            or c == '_' or c == '-' \
            or c == '.' or c == '+'

    def read_unquoted_string(self):
        start = self.cursor
        while self.can_read() and self.is_allowed_in_unquoted_string(self.peek()):
            self.skip()

        return self.string[start:self.cursor]

    def read_quoted_string(self):
        if not self.can_read():
            return ""

        next = self.peek()
        if self.is_quoted_string_start(next):
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_start_of_quote().create_with_context(self)

        self.skip()
        return self.read_string_until(next)

    def read_string_until(self, terminator: str):
        result = ""
        escaped = False
        while self.can_read():
            c = self.read()
            if escaped:
                if c == terminator or c == SYNTAX_ESCAPE:
                    result += c
                    escaped = False
                else:
                    self.set_cursor(self.get_cursor() - 1)
                    raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_invalid_escape().create_with_context(self, str(c))

            elif c == SYNTAX_ESCAPE:
                escaped = True
            elif c == terminator:
                return result
            else:
                result += c

        raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_end_of_quote().create_with_context(self)

    def read_string(self):
        if not self.can_read():
            return ""

        next = self.peek()
        if self.is_quoted_string_start(next):
            self.skip()
            return self.read_string_until(next)

        return self.read_unquoted_string()

    def read_boolean(self):
        start = self.cursor
        value = self.read_string()
        if value == "":
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_bool().create_with_context(self)

        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            self.cursor = start
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_invalid_bool().create_with_context(self, value)

    def expect(self, c):
        if not self.can_read() or self.peek() != c:
            raise CommandSyntaxException.BUILTIN_EXCEPTIONS.reader_expected_symbol().create_with_context(self, str(c))

        self.skip()
