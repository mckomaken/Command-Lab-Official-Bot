from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from lib.commands.blockstate import BlockState
from lib.commands.text import Text
from lib.commands.util import BlockPos, ChunkPos, Vec3d
from lib.commands.util.random import Random
from lib.commands.world import World

T = TypeVar("T")


class TrackedData(Generic[T]):
    v: T

    def __init__(self) -> None:
        super().__init__()


class DataTracker:
    pass


class Box:
    minX: float
    minY: float
    minZ: float
    maxX: float
    maxY: float
    maxZ: float

    def __init__(
        self,
        minX: float,
        minY: float,
        minZ: float,
        maxX: float,
        maxY: float,
        maxZ: float,
    ) -> None:
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ

    @classmethod
    def fromBlockPos(cls, pos: BlockPos):
        return cls(pos.x, pos.y, pos.z, pos.x + 1, pos.y + 1, pos.z + 1)

    @classmethod
    def from2Pos(cls, pos1: Vec3d, pos2: Vec3d):
        return cls(pos1.x, pos1.y, pos1.z, pos2.x, pos2.y, pos2.z)


class RemovalReason(Enum):
    pass


class EntityChangeListener:
    def updateEntityPosition():
        pass

    def remove():
        pass


class EntityDimensions:
    pass


class TrackedPosition:
    pass


class Entity:
    age: int
    AIR: TrackedData[int]
    blockPos: BlockPos
    blockStateAtPos: BlockState
    boundingBox: Box
    changeListener: EntityChangeListener
    chunkPos: ChunkPos
    collidedSoftly: bool
    commandTags: set[str]
    dimensions: EntityDimensions
    distanceTraveled: float
    fallDistance: float
    fireTicks: int
    firstUpdate: bool
    FLAGS: TrackedData[bool]
    forceUpdateSupportingBlockPos: bool
    glowing: bool
    groundCollision: bool
    hasVirtualFire: bool
    horizontalCollision: bool
    horizontalSpeed: float
    id: int
    ignoreCustomFrustum: bool
    inNetherPortal: bool
    inPowderSnow: bool
    intersectionChecked: bool
    invulnerable: bool
    lastChimeAge: int
    lastChimeIntesity: float
    lastNetherPortalPosition: BlockPos
    lastRenderX: float
    lastRenderY: float
    lastRenderZ: float
    movementMultiplier: float
    netherPortalTime: int
    nextStopSoundDistance: float
    noClip: bool
    passengerList: list["Entity"]
    pistonMovementDelta: list[float]
    pistonMovementTick: int
    pitch: float
    portalCooldown: int
    pos: Vec3d
    prevHorizontalSpeed: float
    prevPitch: float
    prevX: float
    prevY: float
    prevYaw: float
    prevZ: float
    random: Random
    removalReason: RemovalReason
    ridingCooldown: int
    speed: float
    standingEyeHeight: float
    stepHeight: float
    submergedFluidTag: set
    submergedInWater: bool
    supportingBlockPos: Optional[BlockPos]
    timeUntilRegen: int
    touchingWater: bool
    trackedPosition: TrackedPosition
    type: "EntityType"
    uuid: UUID
    uuidString: str
    vehicle: "Entity"
    velocity: Vec3d
    velocityDirty: bool
    velocityModified: bool
    verticalCollision: bool
    wasInPowderSnow: bool
    wasOnFire: bool
    world: World
    yaw: float

    def __init__(self, type: "EntityType", world: World):
        self.id = 1
        self.passengerList = list()
        self.velocity = Vec3d.ZERO
        self.boundingBox = Box(0, 0, 0, 0, 0, 0)
        self.movementMultiplier = Vec3d.ZERO
        self.nextStopSoundDistance = 1
        self.random = Random.create()
        self.fireTicks = -self.getBurningDuration()
        self.fluidHeight: list[dict[Any, float]] = list()
        self.submergedFluidTag = set()
        self.firstUpdate = True
        self.changeListener = EntityChangeListener()
        self.trackedPosition = TrackedPosition()

    def is_alive(self):
        return True

    def get_name(self):
        return Text("test")

    def getBurningDuration(self):
        return 0


class EntityType(Enum):
    PLAYER = "player"


class GameMode(Enum):
    SURVIVAL = "survival"
    CREATIVE = "creative"
    ADVENTRUE = "adventure"
    SPECTATOR = "spectator"


class LivingEntity(Entity):
    pass


class PlayerEntity(LivingEntity):
    pass


class ServerPlayerEntity(PlayerEntity):
    pass
