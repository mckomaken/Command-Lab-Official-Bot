from typing import Any
import nbtlib
from lib.commands.reader import StringReader
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.types import ArgumentType


class NbtArgumentType(ArgumentType[dict[str, Any]]):
    def parse(self, reader: StringReader):
        nbt = nbtlib.parse_nbt(reader.read())
        return nbt

    def listSuggestions(self, builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def get_examples(self):
        return []