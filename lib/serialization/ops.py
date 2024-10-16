from typing import overload

from plum import dispatch

from lib.serialization.data_result import DataResult
from lib.util.functions.consumer import BiConsumer, Consumer
from lib.util.number import Number
from lib.util.pair import Pair
from lib.util.stream import Stream


class DynamicOps[T]:
    def empty(self) -> T:
        raise NotImplementedError()

    def emptyMap(self) -> T:
        return

    def emptyList(self) -> T:
        return

    def convertTo[U](self, outOps: "DynamicOps[U]", input: T) -> U:
        raise NotImplementedError()

    @dispatch
    def getNumericValue(self, input: T) -> DataResult[Number]:
        raise NotImplementedError()

    @dispatch
    def getNumericValue(self, input: T, defaultValue: Number) -> DataResult[Number]:
        return self.getNumericValue(input).result().orElse(defaultValue)

    @overload
    def getNumericValue(self, input: T) -> DataResult[Number]: ...
    @overload
    def getNumericValue(self, input: T, defaultValue: Number) -> DataResult[Number]: ...

    def createNumeric(self, i: Number) -> T:
        raise NotImplementedError()

    def createInt(self, value: int) -> T:
        return self.createNumeric(Number(value))

    def createFloat(self, value: float) -> T:
        return self.createNumeric(Number(value))

    def getBooleanValue(self, input: T) -> DataResult[bool]:
        return self.getNumericValue(input).map(bool)

    def createBoolean(self, value: bool) -> T:
        return self.createInt(int(value))

    def getStringValue(self, input: T) -> DataResult[str]:
        raise NotImplementedError()

    def createString(self, value: str) -> T:
        raise NotImplementedError()

    def mergeToList(self, list: T, value: T) -> DataResult[T]:
        raise NotImplementedError()

    def mergeToList(self, list: T, values: list[T]) -> DataResult[T]:
        result: DataResult[T] = DataResult.success(list)

        for value in values:
            result = result.flatMap(lambda r: self.mergeToList(r, value))
        return result

    def mergeToMap(self, map: T, key: T, value: T):
        raise NotImplementedError()

    def getStream(self, var1: T) -> DataResult[Stream[T]]:
        raise NotImplementedError()

    def getList(self, input: T) -> DataResult[Consumer[Consumer[T]]]:
        def _(s: Stream[T]):
            assert s is not None
            return s.forEach

        return self.getStream(input).map(_)

    def createList(self, var1: Stream[T]) -> T:
        raise NotImplementedError()

    def compressMaps(self) -> bool:
        return False

    def getMapValues(self, var1: T) -> DataResult[Stream[Pair[T, T]]]:
        raise NotImplementedError()

    def getMap(self, input: T) -> DataResult[Consumer[BiConsumer[T, T]]]:
        def _(s: Stream[Pair[T, T]]):
            def __(c: BiConsumer[T, T]):
                for p in s:
                    c.accept(p.getLeft(), p.getRight())

            return __

        return self.getMapValues(input).map(_)
