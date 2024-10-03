from lib.commands.reader import StringReader
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.types import ArgumentType
from schemas.data import DataPaths, Items


class ItemArgumentType(ArgumentType[str]):
    def parse(self, reader: StringReader):
        start = reader.getCursor()
        while reader.canRead() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start:reader.cursor]
        return d

    def listSuggestions(self, builder: SuggestionsBuilder):
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