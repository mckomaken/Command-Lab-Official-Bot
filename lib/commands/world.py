import math
from threading import Thread
from typing import Self

from lib.commands.damage import DamageSources
from lib.commands.registry.dynamic import DynamicRegistryManager
from lib.commands.registry.registry_entry import RegistryEntry
from lib.commands.registry.registry_key import RegistryKey
from lib.commands.util import BlockPos
from lib.commands.util.random import Random
from lib.commands.util.supplier import Supplier


class Biome:
    pass


class BiomeStorage:
    def getBiomeForNoiseGen(biomeX: int, biomeY: int, biomeZ: int) -> RegistryEntry[Biome]:
        raise NotImplementedError()


class SeedMixer:
    @staticmethod
    def mixSeed(seed: int, salt: int):
        seed *= seed * 6364136223846793005 + 1442695040888963407
        seed += salt
        return seed


def square(n: float) -> float:
    return n * n


class BiomeAccess:
    storage: BiomeStorage
    seed: int

    def __init__(self, storage: BiomeStorage, seed: int):
        self.storage = storage
        self.seed = seed

    def with_source(self, storage: BiomeStorage):
        return Self(storage, self.seed)

    def getBiome(self, pos: BlockPos) -> RegistryEntry[Biome]:
        i = pos.x - 2
        j = pos.y - 2
        k = pos.z - 2
        l = i >> 2
        m = j >> 2
        n = k >> 2
        d = (i & 3) / 4.0
        e = (j & 3) / 4.0
        f = (k & 3) / 4.0
        o = 0
        g = float("inf")

        for p in range(7):
            bl = (p & 4) == 0
            bl2 = (p & 2) == 0
            bl3 = (p & 1) == 0
            q = bl if l else l + 1
            r = bl2 if m else m + 1
            s = bl3 if n else n + 1
            h = bl if d else d - 1.0
            t = bl2 if e else e - 1.0
            u = bl3 if f else f - 1.0
            v = self.method_38106(self.seed, q, r, s, h, t, u)
            if g > v:
                o = p
                g = v

        p = (o & 4) == 0 if l else l + 1
        w = (o & 2) == 0 if m else m + 1
        x = (o & 1) == 0 if n else n + 1

        return self.storage.getBiomeForNoiseGen(p, w, x)

    @staticmethod
    def method_38108(l: int):
        d = math.modf(l >> 24, 1024) / 1024.0
        return (d - 0.5) * 0.9

    @staticmethod
    def method_38106(l: int, i: int, j: int, k: int, d: float, e: float, f: float):
        m = SeedMixer.mixSeed(l, i)
        m = SeedMixer.mixSeed(m, j)
        m = SeedMixer.mixSeed(m, k)
        m = SeedMixer.mixSeed(m, i)
        m = SeedMixer.mixSeed(m, j)
        m = SeedMixer.mixSeed(m, k)
        g = BiomeAccess.method_38108(m)
        m = SeedMixer.mixSeed(m, l)
        h = BiomeAccess.method_38108(m)
        m = SeedMixer.mixSeed(m, l)
        n = BiomeAccess.method_38108(m)
        return square(f + n) + square(e + h) + square(d + g)


class BlockEntityTickInvoker:
    def tick(self):
        raise NotImplementedError()

    def isRemoved(self) -> bool:
        raise NotImplementedError()

    def getPos(self) -> BlockPos:
        raise NotImplementedError()

    def getName(self) -> str:
        raise NotImplementedError()


class WorldBorder:
    pass


class DimensionType:
    pass


class DimensionEntry:
    pass


class NeighborUpdater:
    pass


class Profiler:
    pass


class WorldProperties:
    pass


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
    registryKey: RegistryKey[Self]
    registryManager: DynamicRegistryManager
    thread: Thread
    thunderGradient: float
    thunderGradientPrev: float
    tickOrder: int


class ServerWorld(World):
    pass
