from brigadier import StringReader
from pydantic import BaseModel

from lib.commands.exceptions import SimpleCommandExceptionType
from lib.commands.text import Text


class InvalidIdentifierException(Exception):
    pass


def is_char_valid(c: str):
    return c >= '0' and c <= '9' or c >= 'a' and c <= 'z' or c == '_' or c == ':' or c == '/' or c == '.' or c == '-'


def is_namespace_character_valid(character: str):
    return character == '_' or character == '-' or character >= 'a' and character <= 'z' or character >= '0' and character <= '9' or character == '.'


def is_path_character_valid(character: str):
    return character == '_' or character == '-' or character >= 'a' and character <= 'z' or character >= '0' \
        and character <= '9' or character == '/' or character == '.'


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
    strings = text.split(':')
    return is_namespace_valid("minecraft" if strings[0] == "" else strings[0]) and is_path_valid(strings[1])


COMMAND_EXCEPTION = SimpleCommandExceptionType(Text.of(""))


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
        i = reader.get_cursor()

        while reader.can_read() and is_char_valid(reader.peek()):
            reader.skip()

        string = reader.get_string()[i:reader.get_cursor()]

        try:
            return cls(string)
        except InvalidIdentifierException:
            reader.set_cursor(i)
            raise COMMAND_EXCEPTION.create_with_context(reader)

    def __str__(self) -> str:
        return f"{self.namespace}:{self.path}"


class Vec3d(BaseModel):
    x: float
    y: float
    z: float

    @property
    def ZERO() -> "Vec3d":
        return Vec3d(0, 0, 0)

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class BlockPos():
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class ChunkPos(BlockPos):
    pass


MAX_INT = 2147483647
MIN_INT = -2147483648
