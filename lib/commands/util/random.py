import time
from typing import Self, overload
from lib.commands.util.supplier import Supplier


def compareAndSet(a, b, c):
    if a == b:
        a = c
        return True
    else:
        return False


class RandomSeed:
    uniquifer: int = 8682522807148012

    @classmethod
    def getSeed(cls):
        cls.uniquifer = cls.uniquifer * 1181783497276652981
        return cls.uniquifer ^ time.time_ns()


class Random:
    seed: Supplier[int]

    @classmethod
    def create(cls) -> Self:
        cls(RandomSeed.getSeed())

    def __init__(self, seed: int):
        self.seed = Supplier.create(seed)

    def next(self, bits: int) -> int:
        L = self.seed.get()
        m = L * 25214903917 + 11 & 281474976710655
        if not compareAndSet(self.seed, L, m):
            raise ValueError("LegacyRandomSource")
        else:
            return m >> 48 - bits

    @overload
    def nextInt(self):
        return self.next(32)

    @overload
    def nextInt(self, bound: int):
        if bound <= 0:
            raise ValueError("Bound must be positive")
        elif (bound & bound - 1) == 0:
            return bound * self.next(31) >> 31
        else:
            i, j = 0, 0
            while (i - j + (bound - 1) < 0):
                i = self.next(31)
                j = i % bound

            return j

    def nextBoolean(self) -> bool:
        return self.next(1) != 0

    def nextFloat(self) -> float:
        return float(self.next(24) * 5.9604645E-8)
