from enum import Enum
from uuid import UUID

from lib.commands.entity import EntityType, LivingEntity
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.world import World


class GameProfile:
    id: UUID
    name: str

    def __init__(self, id: UUID, name: str) -> None:
        self.id = id
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        return self.name


class PlayerEntity(LivingEntity):
    gameProfile: GameProfile

    def __init__(self, world: World, pos: BlockPos, yaw: float, gameProfile: GameProfile):
        super().__init__(EntityType.PLAYER, world)
        self.world = world
        self.uuid = gameProfile.getId()
        self.gameProfile = gameProfile

    def getGameProfile(self):
        return self.gameProfile



class ServerPlayerEntity(PlayerEntity):
    pass


class GameMode(Enum):
    SURVIVAL = "survival"
    CREATIVE = "creative"
    ADVENTRUE = "adventure"
    SPECTATOR = "spectator"