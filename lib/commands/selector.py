import math
from ast import Call
from random import shuffle
from typing import Any, Callable, Coroutine, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from lib.commands import util
from lib.commands.entity import Box, Entity, EntityType, LivingEntity
from lib.commands.exceptions import DynamicCommandExceptionType, SimpleCommandExceptionType
from lib.commands.featureset import FeatureSet
from lib.commands.number_range import FloatRange, IntRange
from lib.commands.player import GameMode, ServerPlayerEntity
from lib.commands.reader import StringReader
from lib.commands.registry.registry import Registries
from lib.commands.registry.registry_key import RegistryKeys
from lib.commands.registry.tag_key import TagKey
from lib.commands.source import CommandSource, ServerCommandSource
from lib.commands.suggestions import Suggestions, SuggestionsBuilder
from lib.commands.text import Text
from lib.commands.util import Identifier, RangeNumberOrNumber
from lib.commands.util.consumer import BiConsumer, Consumer
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.util.mathhelper import MathHelper
from lib.commands.util.predicate import Predicate
from lib.commands.util.type_filter import TypeFilter
from lib.commands.world import ServerWorld

SELECTOR_PREFIX = "@"
ARGUMENTS_OPENING = "["
ARGUMENTS_CLOSING = "]"
ARGUMENT_DEFINER = "="
ARGUMENT_SEPARATOR = ","
INVERT_MODIFIER = "!"
TAG_MODIFIER = "#"
NEAREST_PLAYER = "p"
ALL_PLAYERS = "a"
RANDOM_PLAYER = "r"
SELF = "s"
ALL_ENTITIES = "e"
INVALID_ENTITY_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.invalid"))
UNKNOWN_SELECTOR_EXCEPTION = DynamicCommandExceptionType(
    lambda option: Text.stringifiedTranslatable("argument.entity.selector.unknown", option)
)
NOT_ALLOWED_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.selector.not_allowed"))
MISSING_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.selector.missing"))
UNTERMINATED_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.options.unterminated"))
VALUELESS_EXCEPTION = DynamicCommandExceptionType(
    lambda option: Text.stringifiedTranslatable("argument.entity.options.valueless", option)
)
TOO_MANY_ENTITIES_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.toomany"))
TOO_MANY_PLAYERS_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.player.toomany"))
PLAYER_SELECTOR_HAS_ENTITIES_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.player.entities"))
ENTITY_NOT_FOUND_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.notfound.entity"))
PLAYER_NOT_FOUND_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.notfound.player"))
NOT_ALLOWED_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.selector.not_allowed"))

def NEAREST(pos: Vec3d, entities: list[Entity]):
    entities.sort(key=lambda e: e.squeredDistanceTo(pos))


def FURTHEST(pos: Vec3d, entities: list[Entity]):
    entities.sort(key=lambda e: e.squeredDistanceTo(pos), reverse=True)


def RANDOM(pos: Vec3d, entities: list[Entity]):
    shuffle(list)


def ARBITRARY(pos: Vec3d, entities: list[Entity]):
    pass


def DEFAULT_SUGGESTION_PROVIDER(builder: SuggestionsBuilder, consumer: Callable):
    return builder.build()


class EntitySelector:
    MAX_VALUE = math.inf
    limit: int
    includesNonPlayers: bool
    localWorldOnly: bool
    predicates: list[Predicate[Entity]]
    distance: FloatRange
    positionOffset: Callable[[Vec3d], Vec3d]
    box: Box
    sorter: BiConsumer[Vec3d, list[Entity]]
    senderOnly: bool
    playerName: str
    uuid: str
    entityFilter: TypeFilter[Entity, Any]
    _usesAt: bool

    class _PASSTHROUGH_FILTER(TypeFilter[Entity, Entity]):
        def downcast(self, obj: Any) -> Entity:
            return obj

        def getBaseClass(self):
            return Entity

    PASSTHROUGH_FILTER = _PASSTHROUGH_FILTER()

    def __init__(
        self,
        count,
        includesNonPlayers,
        localWorldOnly,
        predicates,
        distance,
        positionOffset,
        box,
        sorter,
        senderOnly,
        playerName,
        uuid,
        type,
        usesAt,
    ):
        self.limit = count
        self.includesNonPlayers = includesNonPlayers
        self.localWorldOnly = localWorldOnly
        self.predicates = predicates
        self.distance = distance
        self.positionOffset = positionOffset
        self.box = box
        self.sorter = sorter
        self.senderOnly = senderOnly
        self.playerName = playerName
        self.uuid = uuid
        self.entityFilter = self.PASSTHROUGH_FILTER if type is None else type
        self._usesAt = usesAt

    def getLimit(self):
        return self.limit

    def isSenderOnly(self):
        return self.senderOnly

    def isLocalWorldOnly(self):
        return self.localWorldOnly

    def usesAt(self):
        return self._usesAt

    def checkSourcePermission(self, source: ServerCommandSource):
        if self._usesAt and not source.hasPermissionLevel(2):
            raise NOT_ALLOWED_EXCEPTION.create()

    def getEntity(self, source: ServerCommandSource) -> Entity:
        self.checkSourcePermission(source)
        li = self.getEntities(source)
        if len(li) == 0:
            raise ENTITY_NOT_FOUND_EXCEPTION.create()
        elif len(li) > 1:
            raise TOO_MANY_ENTITIES_EXCEPTION.create()
        else:
            return li[0]

    def getEntities(self, source: ServerCommandSource) -> list[Entity]:
        self.checkSourcePermission(source)
        if not self.includesNonPlayers:
            return self.getPlayers(source)
        elif self.playerName is not None:
            serverPlayerEntity = source.getServer().getPlayerManager().getPlayer(self.playerName)
            return list() if serverPlayerEntity is None else [serverPlayerEntity]
        elif self.uuid is not None:
            for serverWorld in source.getServer().getWorlds():
                entity = serverWorld.getEntity(self.uuid)
                if entity is not None:
                    if entity.getType().isEnabled(source.getEnabledFeatures()):
                        return [entity]
                    break

            return []
        else:
            vec3d = self.positionOffset.apply(source.getPosition())
            box = self.getOffsetBox(vec3d)
            if self.senderOnly:
                predicate = self.getPositionPredicate(vec3d, box, None)
                return (
                    [source.getEntity()]
                    if source.getEntity() is not None and predicate.test(source.getEntity())
                    else list()
                )
            else:
                predicate = self.getPositionPredicate(vec3d, box, source.getEnabledFeatures())
                li = list()
                if self.isLocalWorldOnly():
                    self.appendEntitiesFromWorld(li, source.getWorld(), box, predicate)
                else:
                    for serverWorld2 in source.getServer().getWorlds():
                        self.appendEntitiesFromWorld(li, serverWorld2, box, predicate)

                return self.getEntities(vec3d, li)

    def appendEntitiesFromWorld(
        self, entities: list[Entity], world: ServerWorld, box: Optional[Box], predicate: Predicate[Entity]
    ):
        i = self.getAppendLimit()
        if len(entities) < i:
            if box is not None:
                world.collectEntitiesByType(self.entityFilter, box, predicate, entities, i)
            else:
                world.collectEntitiesByType(self.entityFilter, predicate, entities, i)

    def getAppendLimit(self) -> int:
        return self.limit if self.sorter == ARBITRARY else math.inf

    def getPlayer(self, source: ServerCommandSource) -> ServerPlayerEntity:
        self.checkSourcePermission(source)
        li = self.getPlayers(source)
        if len(li) != 1:
            raise PLAYER_NOT_FOUND_EXCEPTION.create()
        else:
            return li[0]

    def getPlayers(self, source: ServerCommandSource) -> list[ServerCommandSource]:
        self.checkSourcePermission(source)
        if self.playerName is not None:
            serverPlayerEntity = source.getServer().getPlayerManager().getPlayer(self.playerName)
            return [] if serverPlayerEntity is None else [serverPlayerEntity]
        elif self.uuid is not None:
            serverPlayerEntity = source.getServer().getPlayerManager().getPlayer(self.uuid)
            return [] if serverPlayerEntity is None else [serverPlayerEntity]
        else:
            vec3d = self.positionOffset.apply(source.getPosition())
            box = self.getOffsetBox(vec3d)
            predicate = self.getPositionPredicate(vec3d, box, None)
            if self.senderOnly:
                var11 = source.getEntity()
                if isinstance(var11, ServerPlayerEntity):
                    serverPlayerEntity2 = var11
                    if predicate.test(serverPlayerEntity2):
                        return [serverPlayerEntity2]

                return []
            else:
                i = self.getAppendLimit()
                if self.isLocalWorldOnly():
                    li = source.getWorld().getPlayers(predicate, i)
                else:
                    li = list()
                    for serverPlayerEntity3 in source.getServer().getPlayerManager().getPlayerList():
                        if predicate.test(serverPlayerEntity3):
                            li.append(serverPlayerEntity3)
                            if len(li) >= i:
                                return li

                return self.getEntities(vec3d, li)

    def getOffsetBox(self, offset: Vec3d) -> Optional[Box]:
        return self.box.offset(offset) if self.box is not None else None

    def getPositionPredicate(self, pos: Vec3d, box: Optional[Box], enabledFeatures: Optional[FeatureSet]):
        bl = enabledFeatures is not None
        bl2 = box is not None
        bl3 = not self.distance.isDummy()
        i = (1 if bl else 0) + (1 if bl2 else 0) + (1 if bl3 else 0)
        li = list()
        if i == 0:
            li = self.predicates
        else:
            li2: list[Predicate[Entity]] = list()
            li2.append(self.predicates)
            if bl:

                def _pred(entity: Entity) -> bool:
                    return entity.getType().isEnabled(enabledFeatures)

                li2.append(_pred)

            if bl2:

                def _pred(entity: Entity) -> bool:
                    return box.intersects(entity.getBoundingBox())

                li2.append(_pred)

            if bl3:

                def _pred(entity: Entity) -> bool:
                    return self.distance.testSqrt(entity.squaredDistanceTo(pos))

                li2.append(_pred)

            li = li2

        return util.allOf(li)

    def getEntities[T](self, pos: Vec3d, entities: list[Entity[T]]) -> list[Entity[T]]:
        if len(entities) > 1:
            self.sorter.accept(pos, entities)

        return entities[: min(self.limit, len(entities))]

    @staticmethod
    def getNames(entities: list[Entity]):
        return Texts.join(entities, Entity.getDisplayName)


class EntitySelectorReader:
    reader: StringReader = None
    atAllowed: bool = None
    limit: int = None
    includesNonPlayers: bool = False
    localWorldOnly: bool = False
    distance: FloatRange = None
    levelRange: IntRange = None
    x: float = None
    y: float = None
    z: float = None
    dx: float = None
    dy: float = None
    dz: float = None
    pitchRange: FloatRange = None
    yawRange: FloatRange = None
    predicates: list[Predicate[Entity]] = list()
    sorter: Callable = None
    senderOnly: bool = False
    playerName: str = None
    startCursor: int = None
    uuid: UUID = None
    suggestionProvider: Callable[[SuggestionsBuilder, Consumer[SuggestionsBuilder]], Suggestions] = None
    selectsName: bool = False
    excludesName: bool = False
    hasLimit: bool = False
    hasSorter: bool = False
    selectsGameMode: bool = False
    excludesGameMode: bool = False
    selectsTeam: bool = False
    excludesTeam: bool = False
    entityType: EntityType = None
    excludesEntityType: bool = False
    selectsScores: bool = False
    selectsAdvancements: bool = False
    usesAt: bool = False

    def __init__(self, reader: StringReader, atAllowed: bool):
        self.distance = FloatRange.any()
        self.levelRange = IntRange.any()
        self.pitchRange = FloatRange.any()
        self.yawRange = FloatRange.any()
        self.predicate = lambda entity: True
        self.sorter = ARBITRARY
        self.suggestionProvider = DEFAULT_SUGGESTION_PROVIDER
        self.reader = reader
        self.atAllowed = atAllowed

    def set_entity_type(self, type: EntityType):
        self.entityType = type

    def readAtVariable(self):
        self.usesAt = True
        self.suggestionProvider = self.suggest_selector_rest
        if not self.reader.canRead():
            raise MISSING_EXCEPTION.createWithContext(self.reader)
        else:
            i = self.reader.getCursor()
            c = self.reader.read()
            if c == "p":
                self.limit = 1
                self.includesNonPlayers = False
                self.sorter = NEAREST
                self.set_entity_type(EntityType.PLAYER)
            elif c == "a":
                self.limit = util.MAX_INT
                self.includesNonPlayers = False
                self.sorter = ARBITRARY
                self.set_entity_type(EntityType.PLAYER)
            elif c == "r":
                self.limit = 1
                self.includesNonPlayers = False
                self.sorter = RANDOM
                self.set_entity_type(EntityType.PLAYER)
            elif c == "s":
                self.limit = 1
                self.includesNonPlayers = True
                self.senderOnly = True
            else:
                if c != "e":
                    self.reader.setCursor(i)
                    UNKNOWN_SELECTOR_EXCEPTION.createWithContext(self.reader, "@" + str(c))

                self.limit = util.MAX_INT
                self.includesNonPlayers = True
                self.sorter = ARBITRARY
                self.predicate = Entity.isAlive

            self.suggestionProvider = self.suggest_open
            if self.reader.canRead() and self.reader.peek() == "[":
                self.reader.skip()
                self.suggestionProvider = self.suggest_option_or_end
                self.read_arguments()

    def readRegular(self):
        if self.reader.canRead():
            self.suggestionProvider = self.suggest_normal

        i: int = self.reader.getCursor()
        string = self.reader.readString()

        try:
            self.uuid = UUID(string)
            self.includesNonPlayers = True
        except Exception:
            if string == "" or len(string) > 16:
                self.reader.setCursor(i)
                raise INVALID_ENTITY_EXCEPTION.createWithContext(self.reader)

            self.includesNonPlayers = False
            self.playerName = string

        self.limit = 1

    def read_arguments(self):
        self.suggestionProvider = self.suggest_option
        self.reader.skipWhitespace()

        while self.reader.canRead() and self.reader.peek() != "]":
            self.reader.skipWhitespace()
            i = self.reader.getCursor()
            string = self.reader.readString()
            selectorHandler = EntitySelectorOptions.get_handler(self, string, i)
            self.reader.skipWhitespace()
            if self.reader.canRead() and self.reader.peek() == "=":
                self.reader.skip()
                self.reader.skipWhitespace()
                self.suggestionProvider = DEFAULT_SUGGESTION_PROVIDER
                selectorHandler.handle(self)
                self.reader.skipWhitespace()
                self.suggestionProvider = self.suggest_end_next
                if not self.reader.canRead():
                    continue

                if self.reader.peek() == ",":
                    self.reader.skip()
                    self.suggestionProvider = self.suggest_option
                    continue

                if self.reader.peek() != "]":
                    raise UNTERMINATED_EXCEPTION.createWithContext(self.reader)
                break

            self.reader.setCursor(i)
            raise VALUELESS_EXCEPTION.createWithContext(self.reader, string)

        if self.reader.canRead():
            self.reader.skip()
            self.suggestionProvider = DEFAULT_SUGGESTION_PROVIDER
        else:
            raise UNTERMINATED_EXCEPTION.createWithContext(self.reader)

    def _suggest_selector(self, builder: SuggestionsBuilder) -> None:
        builder.suggest("@p", Text.translatable("argument.entity.selector.nearestPlayer"))
        builder.suggest("@a", Text.translatable("argument.entity.selector.allPlayers"))
        builder.suggest("@r", Text.translatable("argument.entity.selector.randomPlayer"))
        builder.suggest("@s", Text.translatable("argument.entity.selector.self"))
        builder.suggest("@e", Text.translatable("argument.entity.selector.allEntities"))

    def suggest_selector(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        consumer.accept(builder)
        if self.atAllowed:
            self._suggest_selector(builder)

        return builder.build()

    def suggest_normal(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        suggestionsBuilder = builder.create_offset(self.startCursor)
        consumer.accept(suggestionsBuilder)
        return builder.add(suggestionsBuilder).build()

    def suggest_selector_rest(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        suggestionsBuilder = builder.create_offset(builder.start - 1)
        self.suggest_selector(suggestionsBuilder)
        builder.add(suggestionsBuilder)
        return builder.build()

    def suggest_open(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        builder.suggest(str("["), "")
        return builder.build()

    def suggest_option_or_end(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        builder.suggest(str("]"), "")
        EntitySelectorOptions.suggestOptions(self, builder)
        return builder.build()

    def suggest_option(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        EntitySelectorOptions.suggestOptions(self, builder)
        return builder.build()

    def suggest_end_next(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        builder.suggest(str(","), "")
        builder.suggest(str("]"), "")
        return builder.build()

    def suggestDefinerNext(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        builder.suggest(str("="), "")
        return builder.build()

    def get_reader(self) -> StringReader:
        return self.reader

    def set_predicate(self, condition: Predicate["EntitySelectorReader"]):
        self.predicate = condition

    def read_negation_character(self) -> bool:
        self.reader.skipWhitespace()
        if self.reader.canRead() and self.reader.peek() == "!":
            self.reader.skip()
            self.reader.skipWhitespace()
            return True
        else:
            return False

    def read_tag_character(self) -> bool:
        self.reader.skipWhitespace()
        if self.reader.canRead() and self.reader.peek() == "#":
            self.reader.skip()
            self.reader.skipWhitespace()
            return True
        else:
            return False

    def set_local_world_only(self):
        self.localWorldOnly = True

    def read(self) -> EntitySelector:
        self.startCursor = self.reader.getCursor()
        self.suggestionProvider = self.suggest_selector
        if self.reader.canRead() and self.reader.peek() == "@":
            if not self.atAllowed:
                raise NOT_ALLOWED_EXCEPTION.createWithContext(self.reader)

            self.reader.skip()
            self.readAtVariable()
        else:
            self.readRegular()

        self.buildPredicate()
        return self.build()

    def buildPredicate(self):
        if self.pitchRange != FloatRange.any():
            self.predicates.append(self.rotationPredicate(self.pitchRange, Entity.getPitch))

        if self.yawRange != FloatRange.any():
            self.predicates.append(self.rotationPredicate(self.yawRange, Entity.getYaw))

        if not self.levelRange.isDummy():

            def _pred(entity: Entity):
                return (
                    False
                    if not isinstance(entity, ServerPlayerEntity)
                    else self.levelRange.test(entity.experienceLevel)
                )

            self.predicates.append(_pred)

    def createBox(self, x: float, y: float, z: float):
        bl = x < 0.0
        bl2 = y < 0.0
        bl3 = z < 0.0
        d = x if bl else 0.0
        e = y if bl2 else 0.0
        f = z if bl3 else 0.0
        g = (0.0 if bl else x) + 1.0
        h = (0.0 if bl2 else y) + 1.0
        i = (0.0 if bl3 else x) + 1.0
        return Box(d, e, f, g, h, i)

    def build(self) -> EntitySelector:
        if self.dx is None and self.dy is None and self.dz is None:
            if self.distance.max is not None:
                d = self.distance.max
                box = Box(-d, -d, -d, d + 1.0, d + 1.0, d + 1.0)
            else:
                box = None
        else:
            box = self.createBox(
                0.0 if self.dx is None else self.dx,
                0.0 if self.dy is None else self.dy,
                0.0 if self.dz is None else self.dz,
            )

        if self.x is None and self.y is None and self.z is None:
            funct = lambda pos: pos
        else:
            funct = lambda pos: Vec3d(
                pos.x if self.x is None else self.x,
                pos.y if self.y is None else self.y,
                pos.z if self.z is None else self.z,
            )

        return EntitySelector(
            self.limit,
            self.includesNonPlayers,
            self.localWorldOnly,
            list(self.predicates),
            self.distance,
            funct,
            box,
            self.sorter,
            self.senderOnly,
            self.playerName,
            self.uuid,
            self.entityType,
            self.usesAt,
        )

    def rotationPredicate(self, angleRange: FloatRange, entityToAngle: Callable[[Entity], float]) -> Predicate[Entity]:
        d = MathHelper.wrapDegrees(0.0 if angleRange.min is None else angleRange.min)
        e = MathHelper.wrapDegrees(359.0 if angleRange.max is None else angleRange.max)

        def _pred(entity: Entity):
            f = MathHelper.wrapDegrees(entityToAngle(entity))
            if d > e:
                return f >= d or f <= e
            else:
                return f >= d and f <= e

        return _pred

    def listSuggestions(self, builder: SuggestionsBuilder, consumer: Consumer[SuggestionsBuilder]):
        return self.suggestionProvider(builder.create_offset(self.reader.getCursor()), consumer)


class SelectorHandler:
    def handle(self, reader: EntitySelectorReader):
        raise NotImplementedError()


class SelectorOption:
    handler: SelectorHandler
    condition: Predicate["EntitySelectorOptions"]
    description: Text

    def __init__(
        self,
        handler: SelectorHandler,
        condition: Predicate["EntitySelectorOptions"],
        description: Text,
    ):
        self.handler = handler
        self.condition = condition
        self.description = description


UNKNOWN_OPTION_EXCEPTION = DynamicCommandExceptionType(
    lambda option: Text.stringifiedTranslatable("argument.entity.options.unknown", [option])
)
INAPPLICABLE_OPTION_EXCEPTION = DynamicCommandExceptionType(
    lambda option: Text.stringifiedTranslatable("argument.entity.options.inapplicable", [option])
)
NEGATIVE_DISTANCE_EXCEPTION = SimpleCommandExceptionType(
    Text.translatable("argument.entity.options.distance.negative")
)
NEGATIVE_LEVEL_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.options.level.negative"))
TOO_SMALL_LEVEL_EXCEPTION = SimpleCommandExceptionType(Text.translatable("argument.entity.options.limit.toosmall"))
IRREVERSIBLE_SORT_EXCEPTION = DynamicCommandExceptionType(
    lambda option: Text.stringifiedTranslatable("argument.entity.options.sort.irreversible", [option])
)
INVALID_MODE_EXCEPTION = DynamicCommandExceptionType(
    lambda gamemode: Text.stringifiedTranslatable("argument.entity.options.mode.invalid", [gamemode])
)
INVALID_TYPE_EXCEPTION = DynamicCommandExceptionType(
    lambda entity: Text.stringifiedTranslatable("argument.entity.options.type.invalid", [entity])
)


class EntitySelectorOptions:
    def __init__(self) -> None:
        self.options: dict[str, SelectorOption] = {}
        self.init()

    def put_option(
        self,
        id: str,
        handler: SelectorHandler,
        condition: Predicate[EntitySelectorReader],
        description: Text,
    ):
        self.options[id] = SelectorOption(handler, condition, description)

    @staticmethod
    def get_handler(reader: EntitySelectorReader, string: str, i: int):
        self = EntitySelectorOptions()
        selector_option = self.options.get(string, None)
        if selector_option is not None:
            if selector_option.condition.test(reader):
                return selector_option.handler
            else:
                raise INAPPLICABLE_OPTION_EXCEPTION.createWithContext(reader.get_reader(), string)
        else:
            reader.get_reader().setCursor(i)
            raise UNKNOWN_OPTION_EXCEPTION.createWithContext(reader.get_reader(), string)

    @staticmethod
    def suggestOptions(reader: EntitySelectorReader, builder: SuggestionsBuilder):
        string = builder.remaining.lower()
        self = EntitySelectorOptions()
        for k, v in self.options.items():
            if v.condition.test(reader) and k.lower().startswith(string):
                builder.suggest(f"{k}=", v.description)

    def init(self):
        # ---------------------------------------------------------------------------------

        class NameOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                i = reader.get_reader().getCursor()
                bl = reader.read_negation_character()
                string = reader.get_reader().readString()
                if reader.excludesName and not bl:
                    reader.get_reader().setCursor(i)
                    raise INAPPLICABLE_OPTION_EXCEPTION.createWithContext(reader.get_reader(), "name")
                else:
                    if bl:
                        reader.excludesName = True
                    else:
                        reader.selectsName = True

                    def _predicate(readerx: Entity) -> bool:
                        return (readerx.getName().getString() == string) != bl

                    reader.set_predicate(_predicate)

        self.put_option(
            "name",
            NameOption(),
            Predicate(lambda reader: not reader.selectsName),
            Text.translatable("argument.entity.options.name.description"),
        )

        # ---------------------------------------------------------------------------------

        class DistanceOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                i = reader.get_reader().getCursor()
                doubleRange = FloatRange.parse(reader.get_reader())
                if (doubleRange.min is None or doubleRange.min < 0.0) and (
                    doubleRange.max is None or not doubleRange.max < 0.0
                ):
                    reader.distance = doubleRange
                    reader.set_local_world_only()
                else:
                    reader.get_reader().setCursor(i)
                    raise NEGATIVE_DISTANCE_EXCEPTION.createWithContext(reader.get_reader())

        self.put_option(
            "distance",
            DistanceOption(),
            Predicate(lambda reader: reader.distance.isDummy()),
            Text.translatable("argument.entity.options.distance.description"),
        )

        # ---------------------------------------------------------------------------------

        class LevelOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                i = reader.get_reader().getCursor()
                intRange = IntRange.parse(reader.get_reader())
                if (intRange is None or intRange.min >= 1) and (intRange.max is None or intRange.max >= 0):
                    reader.levelRange = intRange
                    reader.includesNonPlayers = False
                else:
                    reader.get_reader().setCursor(i)
                    raise NEGATIVE_LEVEL_EXCEPTION.createWithContext(reader.get_reader())

        self.put_option(
            "level",
            LevelOption(),
            Predicate(lambda reader: reader.levelRange.isDummy()),
            Text.translatable("argument.entity.options.level.description"),
        )

        # ---------------------------------------------------------------------------------

        class XOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        class YOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        class ZOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        self.put_option(
            "x",
            XOption(),
            Predicate(lambda reader: reader.x is None),
            Text.translatable("argument.entity.options.x.description"),
        )
        self.put_option(
            "y",
            YOption(),
            Predicate(lambda reader: reader.y is None),
            Text.translatable("argument.entity.options.y.description"),
        )
        self.put_option(
            "z",
            ZOption(),
            Predicate(lambda reader: reader.z is None),
            Text.translatable("argument.entity.options.z.description"),
        )

        # ---------------------------------------------------------------------------------

        class DXOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        class DYOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        class DZOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.set_local_world_only()
                reader.x = reader.get_reader().read_float()

        self.put_option(
            "dx",
            DXOption(),
            Predicate(lambda reader: reader.dx is None),
            Text.translatable("argument.entity.options.x.description"),
        )
        self.put_option(
            "dy",
            DYOption(),
            Predicate(lambda reader: reader.dy is None),
            Text.translatable("argument.entity.options.y.description"),
        )
        self.put_option(
            "dz",
            DZOption(),
            Predicate(lambda reader: reader.dz is None),
            Text.translatable("argument.entity.options.z.description"),
        )

        # ---------------------------------------------------------------------------------

        class XRotationOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.pitchRange = math.degrees(FloatRange.parse(reader.get_reader()))

        class YRotationOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                reader.yawRange = math.degrees(FloatRange.parse(reader.get_reader()))

        self.put_option(
            "x_rotation",
            XRotationOption(),
            Predicate(lambda reader: FloatRange.any().test(reader.pitchRange)),
            Text.translatable("argument.entity.options.x_rotation.description"),
        )
        self.put_option(
            "y_rotation",
            YRotationOption(),
            Predicate(lambda reader: FloatRange.any().test(reader.yawRange)),
            Text.translatable("argument.entity.options.y_rotation.description"),
        )

        # ---------------------------------------------------------------------------------

        class LimitOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                i = reader.get_reader().getCursor()
                j = reader.get_reader().read_int()
                if j < 1:
                    reader.get_reader().setCursor(i)
                    raise TOO_SMALL_LEVEL_EXCEPTION.createWithContext(reader.get_reader())
                else:
                    reader.limit = j
                    reader.hasLimit = True

        self.put_option(
            "limit",
            LimitOption(),
            Predicate(lambda reader: not reader.senderOnly and not reader.hasLimit),
            Text.translatable("argument.entity.options.limit.description"),
        )

        # ---------------------------------------------------------------------------------

        class SortOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                i = reader.get_reader().getCursor()
                string = reader.get_reader().readUnquotedString()

                def _provider(builder, consumer):
                    return CommandSource.suggestMatching(("nearest", "furthest", "random", "arbitrary"), builder)

                reader.suggestionProvider = _provider
                if string == "nearest":
                    reader.sorter = NEAREST
                    reader.hasSorter = True
                elif string == "furthest":
                    reader.sorter = FURTHEST
                    reader.hasSorter = True
                elif string == "random":
                    reader.sorter = RANDOM
                    reader.hasSorter = True
                elif string == "arbitrary":
                    reader.sorter = ARBITRARY
                    reader.hasSorter = True
                else:
                    reader.get_reader().setCursor(i)
                    raise IRREVERSIBLE_SORT_EXCEPTION.createWithContext(reader.get_reader(), string)

        self.put_option(
            "sort",
            SortOption(),
            Predicate(lambda reader: not reader.senderOnly and not reader.hasSorter),
            Text.translatable("argument.entity.options.sort.description"),
        )

        # ---------------------------------------------------------------------------------

        class GamemodeOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                def _suggest(builder: SuggestionsBuilder, consumer):
                    string = builder.get_remaining().lower()
                    bl = reader.excludesGameMode
                    bl2 = True
                    if string != "":
                        if string[0] == "!":
                            bl = False
                            string = string[1:]

                    var6 = [n for n in GameMode]
                    for gameMode in var6:
                        if gameMode.value.lower().startswith(string):
                            if bl2:
                                builder.suggest("!" + gameMode.value)

                            if bl:
                                builder.suggest(gameMode.value)

                    return builder.build()

                i = reader.get_reader().getCursor()
                bl = reader.read_negation_character()
                if reader.excludesGameMode and not bl:
                    reader.get_reader().setCursor(i)
                    raise INAPPLICABLE_OPTION_EXCEPTION.createWithContext(reader.get_reader(), "gamemode")
                else:
                    string = reader.get_reader().readUnquotedString()
                    gameMode = next(iter(g for g in GameMode if g == string), None)
                    if gameMode is None:
                        reader.get_reader().setCursor(i)
                        raise INVALID_MODE_EXCEPTION.createWithContext(reader.get_reader(), string)
                    else:

                        def _predicate(entity: Entity) -> bool:
                            if not isinstance(entity, ServerPlayerEntity):
                                return False
                            else:
                                gameMode2 = entity.interactionManager.getGameMode()
                                return gameMode2 != gameMode if not bl else gameMode2 == gameMode

                        reader.includesNonPlayers = False
                        reader.predicate = _predicate
                        if bl:
                            reader.excludesGameMode = True
                        else:
                            reader.selectsGameMode = True

        self.put_option(
            "gamemdoe",
            GamemodeOption(),
            Predicate(lambda reader: not reader.selectsGameMode),
            Text.translatable("argument.entity.options.gamemode.description"),
        )

        class TeamOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                bl = reader.read_negation_character()
                string = reader.get_reader().readUnquotedString()

                def _predicate(entity: Entity):
                    if not isinstance(entity, LivingEntity):
                        return False
                    else:
                        abstractTeam = entity.get_scoreboard_team()
                        string2 = "" if abstractTeam is None else abstractTeam.get_name()
                        return (string2 == string) != bl

                reader.set_predicate(_predicate)

                if bl:
                    reader.excludesTeam = True
                else:
                    reader.selectsTeam = True

        self.put_option(
            "team",
            TeamOption(),
            Predicate(lambda reader: not reader.selectsTeam),
            Text.translatable("argument.entity.options.team.description"),
        )

        class TypeOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                def _suggest(builder: SuggestionsBuilder, consumer):
                    CommandSource.suggest_identifiers(Registries.ENTITY_TYPE.get_ids(), builder, "!")
                    CommandSource.suggest_identifiers(
                        [tag.id for tag in Registries.ENTITY_TYPE.stream_tags()],
                        builder,
                        "!#",
                    )
                    if not reader.excludesEntityType:
                        CommandSource.suggest_identifiers(Registries.ENTITY_TYPE.get_ids(), builder)
                        CommandSource.suggest_identifiers(
                            [tag.id for tag in Registries.ENTITY_TYPE.stream_tags()],
                            builder,
                            "#",
                        )

                    return builder.build()

                reader.suggestionProvider = _suggest

                i = reader.get_reader().getCursor()
                bl = reader.read_negation_character()
                if reader.excludesEntityType and not bl:
                    reader.get_reader().setCursor(i)
                    raise INAPPLICABLE_OPTION_EXCEPTION.createWithContext(reader.get_reader(), "type")
                else:
                    if bl:
                        reader.excludesEntityType = True

                    if reader.read_tag_character():
                        tag_key = TagKey.of(
                            RegistryKeys.ENTITY_TYPE,
                            Identifier.from_command_input(reader.get_reader()),
                        )

                        def _predicate(entity: Entity) -> bool:
                            return entity.type.isIn(tag_key)

                        reader.set_predicate(_predicate)
                    else:
                        identifier = Identifier.from_command_input(reader.get_reader())
                        entity_type = Registries.ENTITY_TYPE.get(identifier)
                        if entity_type is None:
                            reader.get_reader().setCursor(i)
                            return INVALID_TYPE_EXCEPTION.createWithContext(reader.get_reader(), str(identifier))

                        if entity_type == EntityType.PLAYER and not bl:
                            reader.includesNonPlayers = True

                        def _predicate(entity: Entity) -> bool:
                            return (entity.type == entity_type) != bl

                        reader.set_predicate(_predicate)
                        if not bl:
                            reader.entityType = entity_type

        self.put_option(
            "type",
            TypeOption(),
            Predicate(lambda reader: reader.entityType),
            Text.translatable("argument.entity.options.type.description"),
        )

        class TagOption(SelectorHandler):
            def handle(self, reader: EntitySelectorReader):
                bl = reader.read_negation_character()
                string = reader.get_reader().readUnquotedString()

                def _predicate(entity: Entity):
                    if string == "":
                        return (len(entity.commandTags) == 0) != bl
                    else:
                        return (string in entity.commandTags) != bl

                reader.set_predicate(_predicate)

        self.put_option(
            "tag",
            TagOption(),
            Predicate(lambda reader: True),
            Text.translatable("argument.entity.options.tag.description"),
        )

    def description(self) -> Text:
        return self.description