from lib.util.array import Array
from lib.util.array.arrayutil import Arrays
from lib.util.exceptions import IndexOutBoundsException
from lib.util.functions.consumer import Consumer
from lib.util.functions.function import IntFunction
from lib.util.iterator import Iterable, Iterator
from lib.util.spliterator import Spliterator, Spliterators
from lib.util.stream.spined_buffer.abstract import AbstractSpinedBuffer
from lib.util.system import System

MIN_SPINE_SIZE = 8


class SpinedBuffer[E](AbstractSpinedBuffer, Consumer[E], Iterable[E]):
    curChunk: Array[E] | None
    spine: Array[Array[E]] | None

    def __init__(self, initialCapacity: int | None = None) -> None:
        super().__init__(initialCapacity)
        self.curChunk = Array[E](1 << self._initialChunkPower)

    def capacity(self) -> int:
        return (
            self.curChunk.length
            if self._spineIndex == 0
            else self._priorElementCount[self._spineIndex]
            + self.spine[self._spineIndex].length
        )

    def inflateSpine(self) -> None:
        if self.spine is None:
            self.spine = Array[E](MIN_SPINE_SIZE)()
            self._priorElementCount = Array[int](MIN_SPINE_SIZE)
            self.spine[0] = self.curChunk

    def ensureCapacity(self, targetSize: int):
        capacity = self.capacity()
        if targetSize > capacity:
            self.inflateSpine()
            i = self._spineIndex + 1
            while targetSize > capacity:
                i += 1
                if i >= self.spine.length:
                    newSpineSize = self.spine.length * 2
                    self.spine = Arrays.copyOf(self.spine, newSpineSize)
                    self._priorElementCount = Arrays.copyOf(
                        self._priorElementCount, newSpineSize
                    )
                nextChunkSize = self.chunkSize(i)
                self.spine[i] = Array[E](nextChunkSize)
                self._priorElementCount[i] = (
                    self._priorElementCount[i - 1] + self.spine[i - 1].length
                )
                capacity += nextChunkSize

    def increaseCapacity(self):
        self.ensureCapacity(self.capacity() + 1)

    def get(self, index: int) -> E:
        if self._spineIndex == 0:
            if index < self._elementIndex:
                return self.curChunk[index]
            else:
                raise IndexOutBoundsException(str(index))
        if index >= self.count():
            raise IndexOutBoundsException(str(index))

        j: int = 0
        while j <= self._spineIndex:
            j += 1
            if index < self._priorElementCount[j] + self.spine[j].length:
                return self.spine[j][index - self._priorElementCount[j]]

        raise IndexOutBoundsException(str(index))

    def copyInto(self, array: Array[E], offset: int):
        finalOffset = offset + self.count()
        if finalOffset > array.length or finalOffset < offset:
            raise IndexOutBoundsException("does not fit")
        if self._spineIndex == 0:
            System.arraycopy(self.curChunk, 0, array, offset, self._elementIndex)
        else:
            for i in range(self._spineIndex):
                System.arraycopy(self.spine[i], 0, array, offset, self.spine[i].length)
                offset += self.spine[i].length
            if self._elementIndex > 0:
                System.arraycopy(self.curChunk, 0, array, offset, self._elementIndex)

    def asArray(self, arrayFactory: IntFunction[Array[E]]) -> Array[E]:
        size = self.count()
        result = arrayFactory.apply(size)
        self.copyInto(result, 0)
        return result

    def clear(self) -> None:
        if self.spine is not None:
            self.curChunk = self.spine[0]
            for i in range(self.curChunk.length):
                self.curChunk[i] = None
            self.spine = None
            self._priorElementCount = None
        else:
            for i in range(self.curChunk.length):
                self.curChunk[i] = None
        self._spineIndex = 0
        self._elementIndex = 0

    def iterator(self) -> Iterator[E]:
        return Spliterators.iterator(self.spliterator())

    def forEach(self, consumer: Consumer[E]) -> None:
        for j in range(self._spineIndex):
            for t in self.spine[j]:
                consumer.accept(t)

        for i in range(self._elementIndex):
            consumer.accept(self.curChunk[i])

    def accept(self, e: E):
        if self._elementIndex == self.curChunk.length:
            self.inflateSpine()
            if (
                self._spineIndex + 1 >= self.spine.length
                or self.spine[self._spineIndex + 1] is None
            ):
                self.increaseCapacity()
            self._elementIndex = 0
            self._spineIndex += 1
            self.curChunk = self.spine[self._spineIndex]
        self._elementIndex += 1
        self.curChunk[self._elementIndex] = e

    def __str__(self) -> str:
        li = list()
        self.forEach(Consumer(li.add))
        return f"SpinedBuffer: {str(li)}"

    def spliterator(self) -> Spliterator[E]:
        class Splitr(Spliterator[E]):
            splSpineIndex: int
            lastSpineIndex: int
            splElementIndex: int
            lastSpineElementFence: int
            splChunk: Array[E]

            def __init__(
                _self,
                firstSpineIndex: int,
                lastSpineIndex: int,
                firstSpineElementIndex: int,
                lastSpineElementFence: int,
            ) -> None:
                _self.splSpineIndex = firstSpineIndex
                _self.lastSpineIndex = lastSpineIndex
                _self.splElementIndex = firstSpineElementIndex
                _self.lastSpineElementFence = lastSpineElementFence
                assert (
                    self.spine is not None
                    or firstSpineIndex == 0
                    and lastSpineIndex == 0
                )
                _self.splChunk = (
                    self.curChunk if self.spine is None else self.spine[firstSpineIndex]
                )

            def estimateSize(_self) -> int:
                return (
                    _self.lastSpineElementFence - _self.splElementIndex
                    if _self.splSpineIndex == _self.lastSpineIndex
                    else self._priorElementCount[_self.lastSpineIndex]
                    + _self.lastSpineElementFence
                    - self._priorElementCount[_self.splSpineIndex]
                    - _self.splElementIndex
                )

            def characteristics(_self) -> int:
                return Spliterator.SIZED | Spliterator.ORDERED | Spliterator.SUBSIZED

            def tryAdvance(_self, consumer: Consumer[E]):
                if _self.splSpineIndex < _self.lastSpineIndex or (
                    _self.splSpineIndex == _self.lastSpineIndex
                    and _self.splElementIndex < _self.lastSpineElementFence
                ):
                    _self.splElementIndex += 1
                    consumer.accept(_self.splChunk[_self.splElementIndex])
                    if _self.splElementIndex == _self.splChunk.length:
                        _self.splElementIndex = 0
                        _self.splSpineIndex += 1
                        if (
                            self.spine is not None
                            and _self.splSpineIndex <= _self.splSpineIndex
                        ):
                            _self.splChunk = self.spine[_self.splSpineIndex]

                        return True
                return False

            def forEachRemaining(_self, consumer: Consumer[E]):
                if _self.splSpineIndex < _self.lastSpineIndex or (
                    _self.splSpineIndex == _self.lastSpineIndex
                    and _self.splElementIndex < _self.lastSpineElementFence
                ):
                    i = _self.splElementIndex
                    sp = _self.splSpineIndex
                    while sp < _self.lastSpineIndex:
                        sp += 1
                        chunk = self.spine[sp]
                        while i < chunk.length:
                            i += 1
                            consumer.accept(chunk[i])
                        i = 0
                    chunk = (
                        _self.splChunk
                        if _self.splSpineIndex == _self.lastSpineIndex
                        else self.spine[_self.lastSpineIndex]
                    )
                    hElementIndex = int(_self.lastSpineElementFence)
                    for i in range(hElementIndex):
                        consumer.accept(chunk[i])

                    _self.splSpineIndex = _self.lastSpineIndex
                    _self.splElementIndex = _self.lastSpineElementFence

            def trySplit(_self) -> Spliterator[E] | None:
                if _self.splSpineIndex < _self.lastSpineIndex:
                    ret = Splitr(
                        _self.splSpineIndex,
                        _self.lastSpineIndex - 1,
                        _self.splElementIndex,
                        self.spine[_self.lastSpineIndex - 1].length,
                    )
                    _self.splSpineIndex = _self.lastSpineIndex
                    _self.splElementIndex = 0
                    _self.splChunk = self.spine[_self.splSpineIndex]
                    return ret
                elif _self.splSpineIndex == _self.lastSpineIndex:
                    t = int((_self.lastSpineElementFence - _self.splElementIndex) / 2)
                    if t == 0:
                        return None
                    else:
                        ret = Arrays.spliterator(
                            _self.splChunk,
                            _self.splElementIndex,
                            _self.splElementIndex + t,
                        )
                        _self.splElementIndex += t
                        return ret
                else:
                    return None

        return Splitr(0, self._spineIndex, 0, self._elementIndex)
