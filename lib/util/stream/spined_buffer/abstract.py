from abc import ABCMeta, abstractmethod

from lib.util.array import Array

MIN_CHUNK_POWER = 4
MAX_CHUNK_POWER = 30


class AbstractSpinedBuffer(metaclass=ABCMeta):
    _initialChunkPower: int
    _elementIndex: int
    _spineIndex: int
    _priorElementCount: Array[int]

    def __init__(self, initialCapacity: int | None = None) -> None:
        if initialCapacity is None:
            self._initialChunkPower = MIN_CHUNK_POWER
        else:
            self._initialChunkPower = max(MIN_CHUNK_POWER, initialCapacity)

    def isEmpty(self) -> bool:
        return self._spineIndex == 0 and self._elementIndex == 0

    def count(self) -> int:
        return (
            self._elementIndex
            if self._spineIndex == 0
            else self._priorElementCount[self._spineIndex] + self._elementIndex
        )

    def chunkSize(self, n: int) -> int:
        power = (
            self._initialChunkPower
            if n == 0 or n == 1
            else min(self._initialChunkPower + n - 1, MAX_CHUNK_POWER)
        )
        return 1 << power

    @abstractmethod
    def clear(self) -> None:
        pass
