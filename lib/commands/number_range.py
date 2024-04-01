from typing import Callable, Generic, Optional, TypeVar

from brigadier import StringReader
from click import FloatRange

from lib.commands.exceptions import (CommandSyntaxException,
                                     SimpleCommandExceptionType)
from lib.commands.text import Text

EXCEPTION_EMPTY = SimpleCommandExceptionType(Text.translatable("argument.range.empty"))
EXCEPTION_SWAPPED = SimpleCommandExceptionType(Text.translatable("argument.range.swapped"))

T = TypeVar("T", int, float)


def is_next_char_valid(reader: StringReader):
    c = reader.peek()
    if not c.isdigit() and c != '-':
        if c != '.':
            return False
        else:
            return not reader.can_read(2) or reader.peek(1) != '.'
    else:
        return True


class NumberRange(Generic[T]):
    def __init__(self, min: T, max: T):
        self.min = min
        self.max = max

    @staticmethod
    def from_string_reader(reader: StringReader, converter: Callable[[str], T]):
        i = reader.get_cursor()

        while reader.can_read() and is_next_char_valid(reader):
            reader.skip()

        string = reader.get_string()[i:reader.get_cursor()]
        if string == "":
            return None

        return converter(string)

    @classmethod
    def create(self, reader: StringReader, min, max) -> "NumberRange[T]":
        raise NotImplementedError()

    @classmethod
    def parse(cls, commandReader: StringReader, converter: Callable[[str], T]) -> "FloatRange | IntRange":
        i = commandReader.get_cursor()

        try:
            optional = cls.from_string_reader(commandReader, converter)
            if commandReader.can_read(2) and commandReader.peek() == '.' and commandReader.peek(1) == '.':
                commandReader.skip()
                commandReader.skip()
                optional2 = cls.from_string_reader(commandReader, converter)

                if optional is None and optional2 is None:
                    raise EXCEPTION_EMPTY.create_with_context(commandReader)
            else:
                optional2 = optional

            if optional is None and optional2 is None:
                raise EXCEPTION_EMPTY.create_with_context(commandReader)
            else:
                return cls.create(commandReader, optional, optional2)
        except CommandSyntaxException as e:
            commandReader.set_cursor(i)
            raise CommandSyntaxException(e.get_type(), e.get_raw_message(), e.get_input(), i)


class FloatRnage(NumberRange[float]):
    def __init__(self, min: Optional[float], max: Optional[float]) -> None:
        self.min = min
        self.max = max

    @staticmethod
    def create(reader: StringReader, min: str, max: str) -> "FloatRnage":
        if min > max:
            raise EXCEPTION_SWAPPED.create_with_context(reader)
        else:
            return FloatRnage(float(min), float(max))

    @classmethod
    def exactly(cls, value: float) -> "FloatRnage":
        return cls(value, value)

    @classmethod
    def between(cls, min: float, max: float) -> "FloatRnage":
        return cls(min, max)

    @classmethod
    def any(cls) -> "FloatRnage":
        return cls(None, None)

    def test(self, value: float) -> bool:
        if self.min is not None and self.min > value:
            return False
        else:
            return self.max is None or self.max < value

    def is_dummy(self) -> bool:
        return self.max is None and self.min is None

    @staticmethod
    def parse(reader: StringReader) -> "FloatRange":
        return NumberRange.parse(reader, float)


class IntRange(NumberRange[int]):
    def __init__(self, min: Optional[int], max: Optional[int]) -> None:
        self.min = min
        self.max = max

    @classmethod
    def create(cls, reader: StringReader, min: str, max: str) -> "IntRange":
        if min > max:
            raise EXCEPTION_SWAPPED.create_with_context(reader)
        else:
            return IntRange(int(min), int(max))

    @classmethod
    def exactly(cls, value: int) -> "IntRange":
        return cls(value, value)

    @classmethod
    def between(cls, min: int, max: int) -> "IntRange":
        return cls(min, max)

    @classmethod
    def any(cls) -> "IntRange":
        return cls(None, None)

    def test(self, value: int) -> bool:
        if self.min is not None and self.min > value:
            return False
        else:
            return self.max is None or self.max >= value

    def is_dummy(self) -> bool:
        return self.max is None and self.min is None

    @staticmethod
    def parse(reader: StringReader) -> "IntRange":
        return NumberRange.parse(reader, int)
