from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from lib.commands.blockstate import BlockState
from lib.commands.featureset import FeatureSet
from lib.commands.text import Text
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.util.math.chunk_pos import ChunkPos
from lib.commands.util.math.vec3d import Vec3d
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


class Entity[T]():
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

    def isAlive(self):
        return True

    def getName(self):
        return Text("test")

    def getBurningDuration(self):
        return 0

    def getYaw(self):
        return self.yaw

    def getPitch(self):
        return self.pitch

    def getUUID(self):
        return self.uuid

    def getBoundingBox(self):
        return self.boundingBox

    def getType(self):
        return self.type


class EntityType(Enum):
    PLAYER = "player"

    def isEnabled(features: FeatureSet):
        return True


class LivingEntity(Entity):
    pass
