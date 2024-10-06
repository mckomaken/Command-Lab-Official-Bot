from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from lib.commands.exceptions import SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.text import Text
from lib.commands.util.consumer import Consumer
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.util.predicate import Predicate
from lib.commands.util.supplier import Supplier


class InvalidIdentifierException(Exception):
    pass


def is_char_valid(c: str):
    return c >= "0" and c <= "9" or c >= "a" and c <= "z" or c == "_" or c == ":" or c == "/" or c == "." or c == "-"


def is_namespace_character_valid(character: str):
    return (
        character == "_"
        or character == "-"
        or character >= "a"
        and character <= "z"
        or character >= "0"
        and character <= "9"
        or character == "."
    )


def is_path_character_valid(character: str):
    return (
        character == "_"
        or character == "-"
        or character >= "a"
        and character <= "z"
        or character >= "0"
        and character <= "9"
        or character == "/"
        or character == "."
    )


def is_path_valid(path: str):
    for i in range(len(path)):
        if not is_path_character_valid(path[i]):
            return False

    return True


def is_namespace_valid(path: str):
    for i in range(len(path)):
        if not is_namespace_character_valid(path[i]):
            return False

    return True


def is_valid(text: str):
    strings = text.split(":")
    return is_namespace_valid("minecraft" if strings[0] == "" else strings[0]) and is_path_valid(strings[1])


def allOf[T](predicates: list[Predicate[T]]) -> Predicate[T]:
    match len(predicates):
        case 0:
            predicate = lambda _: True
        case 1:
            predicate = predicates[0]
        case 2:
            predicate = predicates[0].And(predicates[1])
        case _:
            predicates2 = list(predicates)

            def predicate(obj: T):
                for pred in predicates2:
                    if not pred.test(obj):
                        return False
                return True

    return predicate


class Util:
    @staticmethod
    def make[T](obj: T, initializer: Consumer[T]) -> T:
        initializer.accept(obj)
        return obj

    @staticmethod
    def makeSupplier[T](factory: Supplier[T]) -> T:
        return factory.get()


COMMAND_EXCEPTION = SimpleCommandExceptionType(Text.of(""))


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class RangedNumber:
    min: int | float
    max: int | float
    original: str

    def __init__(self, cont: str) -> None:
        self.min = cont.split("..", maxsplit=1)[0] or -2147483648
        self.max = cont.split("..", maxsplit=1)[1] or 2147483647
        self.original = cont

    @classmethod
    def __get_validators__(cls):
        yield cls.check

    @classmethod
    def check(cls, cont: str):
        if ".." in cont:
            raise TypeError("Invalid range number")
        _min = cont.split("..", maxsplit=1)[0]
        _max = cont.split("..", maxsplit=1)[1]

        if not (_min.isdigit() or (_min.replace(".", "", 1).isdigit() and _min.count(".") < 2)):
            raise TypeError("Invalid minimum value of range number")

        if not (_max.isdigit() or (_max.replace(".", "", 1).isdigit() and _max.count(".") < 2)):
            raise TypeError("Invalid maximum value of range number")

        return cont

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


RangeNumberOrNumber = RangedNumber | float | int


class Identifier:
    def __init__(self, namespace: str, path: str = None) -> None:
        self.namespace = "minecraft" if path is None else namespace
        self.path = path

    def get_namespace(self):
        return self.namespace

    def get_path(self):
        return self.path

    @classmethod
    def try_parse(cls, text: str):
        splitted = text.split(":", maxsplit=1)
        if len(splitted) != 2:
            raise ValueError("Invalid identifier")

        cls(splitted[0], splitted[1])

    @classmethod
    def from_command_input(cls, reader: StringReader):
        i = reader.getCursor()

        while reader.canRead() and is_char_valid(reader.peek()):
            reader.skip()

        string = reader.getString()[i : reader.getCursor()]

        try:
            return cls(string)
        except InvalidIdentifierException:
            reader.setCursor(i)
            raise COMMAND_EXCEPTION.createWithContext(reader)

    def __str__(self) -> str:
        return f"{self.namespace}:{self.path}"

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


class ChunkPos(BlockPos):
    pass


class Vec2f:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


MAX_INT = 2147483647
MIN_INT = -2147483648
