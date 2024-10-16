from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum

from plum import dispatch

from lib.util.exceptions import IllegalStateException
from lib.util.functions.consumer import Consumer, IntConsumer
from lib.util.functions.function import Function
from lib.util.functions.predicate import Predicate
from lib.util.iterator import Iterator
from lib.util.map import Map
from lib.util.spliterator import OfInt, Spliterator
from lib.util.stream.spined_buffer import SpinedBuffer


class BaseStream[T, S](metaclass=ABCMeta):
    @abstractmethod
    def iterator(self) -> Iterator[T]:
        pass

    @abstractmethod
    def isParallel(self) -> bool:
        pass

    @abstractmethod
    def sequential(self) -> S:
        pass

    @abstractmethod
    def parallel(self) -> S:
        pass

    @abstractmethod
    def unordered(self) -> S:
        pass

    @abstractmethod
    def close(self):
        pass


class Stream[T](BaseStream[T, "Stream[T]"]):
    _internal: list[T]
    _i: int

    def __init__(self) -> None:
        self._internal = []
        self._i = 0

    def filter(self, predicate: Predicate[T]) -> Stream[T]:
        def _(obj: T):
            return predicate.test(obj)

        self._internal = list(filter(_, list(self._internal)))
        return self

    def map[R](self, mapper: Function[T, R]) -> Stream[R]:
        for i, e in enumerate(list(self._internal)):
            e[i] = mapper.apply(e)

    def forEach(self, action: Consumer[T]):
        for e in list(self._internal):
            action.accept(e)

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == len(self._internal):
            raise StopIteration()
        elm = self._internal[self._i]
        self._i += 1
        return elm

    def iterator(self) -> Iterator[T]:
        return Iterator(self._internal)

    @staticmethod
    def of[_T](t: _T) -> Stream[_T]:
        pass

    class Builder[_T](Consumer[_T], metaclass=ABCMeta):
        @abstractmethod
        def accept(self, v: _T):
            pass

        def add(self, t: _T) -> Stream.Builder[_T]:
            self.accept(t)
            return self

        @abstractmethod
        def build(self) -> Stream[_T]:
            pass


class Streams:
    def __init__(self) -> None:
        raise NotImplementedError("No instances")

    class RangeIntSpliterator(OfInt):
        _from: int
        _upTo: int
        _last: int

        BALANCED_SPLIT_THRESHOLD = 1 << 24
        RIGHT_BALANCED_SPLIT_RATIO = 1 << 3

        @dispatch
        def __init__(self, _from: int, upTo: int, closed: bool) -> None:
            self._from = _from
            self._upTo = upTo
            self._last = 1 if closed else 0

        @dispatch
        def __init__(self, _from: int, upTo: int, last: int) -> None:
            self._from = _from
            self._upTo = upTo
            self._last = last

        def tryAdvance(self, action: IntConsumer) -> bool:
            i = int(self._from)
            if i < self._upTo:
                self._from += 1
                action.accept(i)
                return True
            elif self._last > 0:
                self._last = 0
                action.accept(i)
                return True
            return False

        def forEachRemaining(self, action: IntConsumer):
            i = int(self._from)
            hUpTo = int(self._upTo)
            hLast = int(self._last)
            self._from = self._upTo
            self._last = 0

            while i < hUpTo:
                i += 1
                action.accept(i)
            if hLast > 0:
                action.accept(i)

        def estimateSize(self) -> int:
            return self._upTo - self._from + self._last

        def _characteristics(self) -> int:
            return (
                Spliterator.ORDERED
                | Spliterator.SIZED
                | Spliterator.SUBSIZED
                | Spliterator.IMMUTABLE
                | Spliterator.NONNULL
                | Spliterator.DISTINCT
                | Spliterator.SORTED
            )

        def trySplit(self) -> Spliterator.OfInt:
            size = self.estimateSize()
            f = int(self._from)
            self._from = self._from + self.splitPoint(size)
            return None if size <= 1 else Streams.RangeIntSpliterator(f, self._from, 0)

        def splitPoint(self, size: int) -> int:
            d = (
                2
                if size < self.BALANCED_SPLIT_THRESHOLD
                else self.RIGHT_BALANCED_SPLIT_RATIO
            )
            return int(size / d)


class AbstractStreamBuilderImpl[T, S: Spliterator[T]](Spliterator[T]):
    count: int

    def trySplit(self) -> Spliterator[T]:
        return None

    def estimateSize(self) -> int:
        return -self.count - 1

    def _characteristics(self) -> int:
        return (
            Spliterator.SIZED
            | Spliterator.SUBSIZED
            | Spliterator.ORDERED
            | Spliterator.IMMUTABLE
        )


class StreamBuilderImpl[T](
    AbstractStreamBuilderImpl[T, Spliterator[T]], Stream.Builder[T]
):
    first: T
    count: int
    buffer: SpinedBuffer[T]

    @dispatch
    def __init__(self) -> None:
        pass

    @dispatch
    def __init__(self, t: T):
        self.first = t
        self.count = -2

    def accept(self, t: T):
        if self.count == 0:
            self.first = t
            self.count += 1
        elif self.count > 0:
            if self.buffer is None:
                self.buffer = SpinedBuffer()
                self.buffer.accept(self.first)
                self.count += 1
            self.buffer.accept(t)
        else:
            raise IllegalStateException()

    def add(self, t: T) -> Stream.Builder[T]:
        self.accept(t)
        return self

    def build(self) -> Stream[T]:
        c = int(self.count)
        if c >= 0:
            self.count = -self.count - 1
            if c < 2:
                StreamSupport.stream()
            else:
                pass
        raise IllegalStateException()

    def tryAdvance(self, action: Consumer[T]):
        if self.count == -2:
            action.accept(self.first)
            self.count = -1
            return True
        else:
            return False

    def forEachRemaining(self, action: Consumer[T]):
        if self.count == -2:
            action.accept(self.first)
            self.count = -1


class StreamOpFlag(Enum):
    DISTINCT = (0, set())

    class Type(Enum):
        SPLITERATOR = 0
        STREAM = 1
        OP = 2
        TERMINAL_OP = 3
        UPSTREAM_TERMINAL_OP = 4

    class MaskBuilder:
        SET_BITS = 0b01
        CLEAR_BITS = 0b10
        PRESERVE_BITS = 0b11

        def __init__(self, map: Map[StreamOpFlag.Type, int]) -> None:
            self.map = map

        def mask(self, t: StreamOpFlag.Type, i: int) -> StreamOpFlag.MaskBuilder:
            self.map
            return self

        def set(self, t: StreamOpFlag.Type):
            return self.mask(t, self.SET_BITS)

        def set(self, t: StreamOpFlag.Type):
            return self.mask(t, self.CLEAR_BITS)

        def setAndClear(self, t: StreamOpFlag.Type):
            return self.mask(t, self.PRESERVE_BITS)

        def build(self) -> Map[StreamOpFlag.Type, int]:
            for t in StreamOpFlag.Type:
                self.map.putIfAbsent(t, 0b00)
            return self.map

    @staticmethod
    def set(t: StreamOpFlag.Type) -> MaskBuilder:
        return StreamOpFlag.MaskBuilder(EnumMap(Type)).set(t)

class StreamSupport:
    def __init__(self) -> None:
        pass

    @staticmethod
    def stream[T](spliterator: Spliterator[T], parallel: bool) -> Stream[T]:
        return
