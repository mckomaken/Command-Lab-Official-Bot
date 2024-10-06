from typing import Self
from lib.commands.context import CommandContext
from lib.commands.entity import Entity
from lib.commands.exceptions import SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.selector import EntitySelector, EntitySelectorReader
from lib.commands.source import ServerCommandSource
from lib.commands.text import Text
from lib.commands.types import ArgumentType


TOO_MANY_ENTITIES_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.toomany"))
TOO_MANY_PLAYERS_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.player.toomany"))
PLAYER_SELECTOR_HAS_ENTITIES_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.player.entities"))
ENTITY_NOT_FOUND_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.notfound.entity"))
PLAYER_NOT_FOUND_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.notfound.player"))
NOT_ALLOWED_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.selector.not_allowed"))


class EntityArgumentType(ArgumentType[EntitySelector]):
    EXAMPLES = ["Player", "0123", "@e", "@e[type=foo]", "dd12be42-52a9-4a91-a8a1-11c01849e498"]
    singleTarget: bool
    playersOnly: bool

    def __init__(self, singleTarget: bool, playersOnly: bool) -> None:
        super().__init__()
        self.singleTarget = singleTarget
        self.playersOnly = playersOnly

    @staticmethod
    def entity() -> Self:
        return EntityArgumentType(True, False)

    @staticmethod
    def getEntity(context: CommandContext[ServerCommandSource], name: str) -> Entity:
        return context.getArgument(name, EntitySelector)

    @staticmethod
    def entities() -> Self:
        return EntityArgumentType(False, False)

    @staticmethod
    def getEntities(context: CommandContext[ServerCommandSource], name: str) -> list[Entity]:
        return []

    @staticmethod
    def getOptionalEntities(context: CommandContext[ServerCommandSource], name: str) -> list[Entity]:
        pass

    @staticmethod
    def getOptionalPlayers(context: CommandContext[ServerCommandSource], name: str) -> list[Entity]:
        pass

    @staticmethod
    def player() -> Self:
        return EntityArgumentType(True, True)

    @staticmethod
    def players() -> Self:
        return EntityArgumentType(False, True)

    def parse(self, reader: StringReader) -> EntitySelector:
        i = False
        entitySelectorReader = EntitySelectorReader(reader, True)
        entitySelector = entitySelectorReader.read()
