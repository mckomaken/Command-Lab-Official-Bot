from lib.commands.context import CommandContext
from lib.commands.exceptions import DynamicCommandExceptionType, SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.registry.registry import Registries
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.types import ArgumentType
from lib.commands.util.consumer import Consumer
from schemas.data import DataPaths, Items

INVALID_ITEM_ID_EXCEPTION = DynamicCommandExceptionType(
    lambda id: Text.stringifiedTranslatable("argument.item.id.invalid", [id])
)
UNKNOWN_COMPONENT_EXCEPTION = DynamicCommandExceptionType(
    lambda id: Text.stringifiedTranslatable("arguments.item.component.unknown", [id])
)
COMPONENT_EXPECTED_EXCEPTION = SimpleCommandExceptionType(Text.translatable("arguments.item.component.expected"))
REPEATED_COMPONENT_EXCEPTION = DynamicCommandExceptionType(
    lambda type: Text.stringifiedTranslatable("arguments.item.component.repeated", [type])
)
MALFORMED_ITEM_EXCEPTION = DynamicCommandExceptionType(
    lambda error: Text.stringifiedTranslatable("arguments.item.malformed", [error])
)
MALFORMED_COMPONENT_EXCEPTION = DynamicCommandExceptionType(
    lambda type, error: Text.stringifiedTranslatable("arguments.item.component.malformed", [type, error])
)

OPEN_SQUARE_BRACKET = "["
CLOSED_SQUARE_BRACKET = "]"
COMMA = ","
EQUAL_SIGN = "="
EXCLAMATION_MARK = "!"


class ItemStringReader:
    def __init__(self) -> None:
        self.itemRegistry = Registries.ITEM


class ItemArgumentType(ArgumentType[str]):
    def parse(self, reader: StringReader):
        start = reader.getCursor()
        while reader.canRead() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start : reader.cursor]
        return d

    async def listSuggestions[S](self, context: CommandContext[S], builder: SuggestionsBuilder):
        return Suggestions.EMPTY

    def getExamples(self):
        result = []
        with open("./minecraft_data/data/dataPaths.json") as fp:
            dataPath = DataPaths.model_validate_json(fp.read())
            with open("./minecraft_data/data/" + dataPath.pc["1.20.4"].items + "/items.json") as fp2:
                items = Items.model_validate_json(fp2.read())
                for item in items.root:
                    result.append(f"minecraft:{item.name}")
        return result
