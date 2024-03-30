from threading import Thread
from .util.random import Random
from .util.supplier import Supplier


class World:
    ambientDarkness: int
    biomeAccess: BiomeAccess
    blockEntityTickers: list[BlockEntityTickInvoker]
    border: WorldBorder
    damageSources: DamageSources
    debugWorld: bool
    dimension: DimensionType
    dimensionEntry: DimensionEntry
    isClient: bool
    iteratingTickingBlockEntities: bool
    lcgBlockSeed: int
    lcgBlockSeedIncrement: int
    neighborUpdater: NeighborUpdater
    pendingBlockEntityTickers: list[BlockEntityTickInvoker]
    profiler: Supplier[Profiler]
    properties: WorldProperties
    rainGradient: float
    rainGradientPrev: float
    random: Random
    registryKey:
    registryManager: DynamicRegistryManager
    thread: Thread
    thunderGradient: float
    thunderGradientPrev: float
    tickOrder: int
