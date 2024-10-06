import re

from lib.commands.exceptions import CommandSyntaxException
from lib.commands.reader import StringReader
from lib.commands.selector import EntitySelector
from lib.commands.suggestions import SuggestionsBuilder
from lib.commands.types import ArgumentType

SELECTOR_PATTERN = re.compile(
    r"(@e|@s|@r|@p|@a)\[((target|distance|x|y|z|dx|dy|dz|scores|tag|team|limit|sort|level|gamemode|x_rotation|y_rotation|type|nbt|advancements|predicate)=(.+?))*\]"
)


class SelectorArgumentType(ArgumentType[EntitySelector]):
    def parse(self, reader: StringReader):
        start = reader.getCursor()
        while reader.canRead() and reader.peek() != " ":
            reader.skip()

        d = reader.string[start : reader.cursor]
        gps = SELECTOR_PATTERN.match(d)
        if gps is None:
            raise CommandSyntaxException(message="Selector Error")

        atX = gps.group(0)
        if atX == "@e":
            selector = EntitySelector(target="all_entities")
        elif atX == "@p":
            selector = EntitySelector(target="nearest_player")
        elif atX == "@a":
            selector = EntitySelector(target="all_players")
        elif atX == "@r":
            selector = EntitySelector(target="random_player")
        elif atX == "@s":
            selector = EntitySelector(target="nearest_player")
        else:
            raise CommandSyntaxException(message="Selector Error")

        for gpIndex in range(2, len(gps.groups()) - 2, 2):
            key = gps.group(gpIndex)
            value = gps.group(gpIndex + 1)

            if key is None or value is None:
                raise CommandSyntaxException(message="Selector Error")

        return selector

    def listSuggestions(self, builder: SuggestionsBuilder):
        builder.add("@a")
        builder.add("@p")
        builder.add("@e")
        builder.add("@r")
        builder.add("@s")
        return builder.build()

    def getExamples(self):
        return ["@p", "@r", "@a", "@e", "@s"]
