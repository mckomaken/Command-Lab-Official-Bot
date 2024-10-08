import asyncio
from typing import Self

from lib.commands.context import CommandContext
from lib.commands.entity import Entity
from lib.commands.exceptions import CommandSyntaxException, SimpleCommandExceptionType
from lib.commands.reader import StringReader
from lib.commands.selector import EntitySelector, EntitySelectorReader
from lib.commands.source import CommandSource, ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.types import ArgumentType
from lib.commands.util.consumer import Consumer

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
        entitySelectorReader = EntitySelectorReader(reader, True)
        entitySelector = entitySelectorReader.read()

        if entitySelector.getLimit() > 1 and self.singleTarget:
            if self.playersOnly:
                reader.setCursor(0)
                raise TOO_MANY_PLAYERS_EXCEPTION.createWithContext(reader)
            else:
                reader.setCursor(0)
                raise TOO_MANY_ENTITIES_EXCEPTION.createWithContext(reader)
        elif entitySelector.includesNonPlayers and self.playersOnly and not entitySelector.isSenderOnly():
            reader.setCursor(0)
            raise PLAYER_SELECTOR_HAS_ENTITIES_EXCEPTION.createWithContext(reader)
        else:
            return entitySelector

    async def listSuggestions[S](self, context: CommandContext[S], builder: SuggestionsBuilder):
        commandSource = context.get_source()
        if isinstance(commandSource, CommandSource):
            stringReader = StringReader(builder.getInput())
            stringReader.setCursor(builder.getStart())
            entitySelectorReader = EntitySelectorReader(stringReader, True)
            try:
                entitySelectorReader.read()
            except CommandSyntaxException as e:
                raise e

            def _consumer1(builderx: SuggestionsBuilder):
                collection = commandSource.getPlayerNames()
                iterable = collection if self.playersOnly else (collection + commandSource.getEntitySuggestions())
                asyncio.create_task(CommandSource.suggestMatching(iterable, builderx))

            return await entitySelectorReader.listSuggestions(builder, Consumer(_consumer1))
        else:
            return Suggestions.EMPTY