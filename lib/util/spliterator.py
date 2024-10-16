from __future__ import annotations

import copy
from abc import ABCMeta, abstractmethod
from typing import Any

from plum import dispatch

from lib.util.collection import Collection
from lib.util.exceptions import NoSuchElementException, NullPointerException
from lib.util.functions.consumer import Consumer, FloatConsumer, IntConsumer
from lib.util.iterator import Iterable, Iterator


class Spliterator[T](metaclass=ABCMeta):
    ORDERED = 0x00000010
    DISTINCT = 0x00000001
    SORTED = 0x00000004
    SIZED = 0x00000040
    NONNULL = 0x00000100
    IMMUTABLE = 0x00000400
    CONCURRENT = 0x00001000
    SUBSIZED = 0x00004000

    @abstractmethod
    def tryAdvance(self, action: Consumer[T]):
        pass

    def forEachRemaining(self, action: Consumer[T]):
        while self.tryAdvance(action):
            continue

    @abstractmethod
    def trySplit(self) -> Spliterator[T]:
        pass

    @abstractmethod
    def estimateSize(self) -> int:
        pass

    @abstractmethod
    def characteristics(self) -> int:
        pass

    def getExactSizeIfKnown(self) -> int:
        return -1 if self.characteristics() == 0 else self.estimateSize()

    def hasCharacteristics(self, characteristics: int) -> bool:
        return (self.characteristics() & characteristics) == characteristics


class OfPrimitive[
    T2,
    T_CONS,
    T_SPLITER,
](Spliterator[T2], metaclass=ABCMeta):
    @abstractmethod
    def trySplit(self) -> Spliterator.OfPrimitive[T2, T_CONS, T_SPLITER]:
        pass

    @abstractmethod
    def tryAdvance(self, action: T_CONS) -> bool:
        pass

    def forEachRemaining(self, action: T_CONS) -> None:
        while self.tryAdvance(action):
            continue


class OfInt(OfPrimitive[int, IntConsumer, "OfInt"], metaclass=ABCMeta):
    @abstractmethod
    def trySplit(self) -> OfInt:
        pass

    @abstractmethod
    def tryAdvance(self, action: IntConsumer) -> bool:
        pass

    def forEachRemaining(self, action: IntConsumer):
        while self.tryAdvance(action):
            continue


class OfFloat(OfPrimitive[float, FloatConsumer, "OfFloat"], metaclass=ABCMeta):
    @abstractmethod
    def trySplit(self) -> OfFloat:
        pass

    @abstractmethod
    def tryAdvance(self, action: FloatConsumer) -> bool:
        pass

    def forEachRemaining(self, action: FloatConsumer):
        while self.tryAdvance(action):
            continue


class Spliterators:
    def __init__(self) -> None:
        pass

    @staticmethod
    def emptySpliterator[T]():
        return Spliterators.EmptySpliterator()

    class EmptySpliterator[T, S, C]:
        def __init__(self) -> None:
            pass

        def trySplit(self) -> S | None:
            return None

        def tryAdvance(self, consumer: C):
            return False

        def forEachRemaining(self, consumer: C):
            pass

        def estimateSize(self):
            return 0

        def characteristics(self):
            return Spliterator.SIZED | Spliterator.SUBSIZED

    class OfRef[T](EmptySpliterator[T, Spliterator[T], Consumer[T]], Spliterator[T]):
        def __init__(self) -> None:
            pass

    class ArraySpliterator[T](Spliterator[T]):
        array: list[Any]
        index: int
        fence: int
        _characteristics: int
        _estimatedSize: int

        @dispatch
        def __init__(self, array: list[Any], additionalCharacteristics: int) -> None:
            self.array = array
            self.index = 0
            self.fence = len(array)
            self._characteristics = (
                additionalCharacteristics | Spliterator.SIZED | Spliterator.SUBSIZED
            )
            self._estimatedSize = -1

        @dispatch
        def __init__(
            self,
            array: list[Any],
            origin: int,
            fence: int,
            additionalCharacteristics: int,
        ) -> None:
            self.array = array
            self.index = origin
            self.fence = fence
            self._characteristics = (
                additionalCharacteristics | Spliterator.SIZED | Spliterator.SUBSIZED
            )
            self._estimatedSize = -1

        @dispatch
        def __init__(
            self,
            array: list[Any],
            origin: int,
            fence: int,
            additionalCharacteristics: int,
            estimatedSize: int,
        ) -> None:
            self.array = array
            self.index = origin
            self.fence = fence
            self._characteristics = additionalCharacteristics & ~(
                Spliterator.SIZED | Spliterator.SUBSIZED
            )
            self._estimatedSize = estimatedSize

        def trySplit(self) -> Spliterator[T]:
            lo = self.index
            mid = lo + self.fence >> 1
            if lo >= mid:
                return None
            if self._estimatedSize == -1:
                self.index = mid
                return Spliterators.ArraySpliterator(
                    self.array, lo, self.index, self._characteristics
                )
            prefixEstimatedSize = self._estimatedSize >> 1
            self._estimatedSize -= prefixEstimatedSize
            self.index = mid
            return Spliterators.ArraySpliterator(
                self.array, lo, self.index, self._characteristics, prefixEstimatedSize
            )

        def forEachRemaining(self, action: Consumer[T]):
            if action is None:
                raise NullPointerException()
            a = self.array
            hi = self.fence
            i = self.index
            self.index = hi
            if len(a) >= hi and i >= 0 and i < hi:
                i += 1
                while i < hi:
                    action.accept(a[i])

        def tryAdvance(self, action: Consumer[T]):
            if action is None:
                raise NullPointerException()
            if self.index >= 0 and self.index < self.fence:
                self.index += 1
                e = self.array[self.index]
                action.accept(e)
                return True
            return False

        def estimateSize(self) -> int:
            return (
                self._estimatedSize
                if self._estimatedSize >= 0
                else self.fence - self.index
            )

        def characteristics(self) -> int:
            return self._characteristics

    class IteratorSpliterator[T](Spliterator[T]):
        BATCH_UNIT = 1 << 10
        MAX_BATCH = 1 << 25

        collection: Collection[T]
        it: Iterator[T]
        _characteristics: int
        est: int
        batch: int

        @dispatch
        def __init__(self, collection: Collection[T], characteristics: int) -> None:
            self.collection = collection
            self.it = None
            self._characteristics = (
                characteristics | Spliterator.SIZED | Spliterator.SUBSIZED
                if (characteristics & Spliterator.CONCURRENT) == 0
                else characteristics
            )

        @dispatch
        def __init__(self, iterator: Iterator[T], size: int, characteristics: int):
            self.collection = None
            self.it = iterator
            self.size = size
            self._characteristics = (
                characteristics | Spliterator.SIZED | Spliterator.SUBSIZED
                if (characteristics & Spliterator.CONCURRENT) == 0
                else characteristics
            )

        @dispatch
        def __init__(self, iterator: Iterator[T], characteristics: int):
            self.collection = None
            self.it = iterator
            self.est = 0x7FFFFFFFFFFFFFFF
            self._characteristics = characteristics & ~(
                Spliterator.SIZED | Spliterator.SUBSIZED
            )

        def trySplit(self) -> Spliterator[T]:
            i = self.it
            if i is None:
                i = self.it = self.collection.iterator()
                s = self.est = self.collection.size()
            else:
                s = self.est

            if s > 1 and i.hasNext():
                n = self.batch + self.BATCH_UNIT
                if n > s:
                    n = int(s)
                if n > self.MAX_BATCH:
                    n = self.MAX_BATCH
                a: list[Any] = list()
                j = 1
                while j < n and i.hasNext():
                    j += 1
                    a[j] = i.next()
                self.batch = j
                if self.est != 0x7FFFFFFFFFFFFFFF:
                    self.est -= j
                    return Spliterators.ArraySpliterator(a, 0, j, self._characteristics)
                return Spliterators.ArraySpliterator(
                    a, 0, j, self._characteristics, 0x7FFFFFFFFFFFFFFF / 2
                )
            return None

        def forEachRemaining(self, action: Consumer[T]):
            if action is None:
                return NullPointerException()
            i = self.it
            if i is None:
                i = self.it = self.collection.iterator()
                self.est = self.collection.size()
            i.forEachRemaining(action)

        def tryAdvance(self, action: Consumer[T]):
            if action is None:
                return NullPointerException()
            if self.it is None:
                self.it = self.collection.iterator()
                self.est = self.collection.size()
            if self.it.hasNext():
                action.accept(self.it.next())
                return True
            return False

        def estimateSize(self) -> int:
            if self.it is None:
                self.it = self.collection.iterator()
                self.est = self.collection.size()
                return self.est
            return self.est

        def characteristics(self) -> int:
            return self._characteristics

    @staticmethod
    def spliteratorUnknownSize[T](
        iterator: Iterator[T], characteristics: int
    ) -> Spliterator[T]:
        return Spliterators.IteratorSpliterator(iterator, characteristics)

    @staticmethod
    def spliterator[T](c: Collection[T], characteristics: int) -> Spliterator[T]:
        return Spliterators.IteratorSpliterator(c, characteristics)

    @staticmethod
    def iterator[T](spliterator: Spliterator[T]) -> Iterator[T]:
        class Adapter(Iterator[T], Consumer[T]):
            valueReady: bool
            nextElement: T

            def __init__(self) -> None:
                self.valueReady = False
                self.nextElement = None

            def accept(self, v: T):
                self.valueReady = True
                self.nextElement = v

            def hasNext(self) -> bool:
                if not self.valueReady:
                    spliterator.tryAdvance(self)
                return self.valueReady

            def next(self) -> T:
                if not self.valueReady and not self.hasNext():
                    raise NoSuchElementException()
                else:
                    self.valueReady = False
                    t = copy.copy(self.nextElement)
                    self.nextElement = None
                    return t

            def forEachRemaining(self, action: Consumer[T]):
                if self.valueReady:
                    self.valueReady = False
                    t = copy.copy(self.nextElement)
                    self.nextElement = None
                    action.accept(t)
                spliterator.forEachRemaining(action)

        return Adapter()
