from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING
from plum import dispatch

from lib.serialization.data_result import DataResult
from lib.serialization.ops import DynamicOps
from lib.util.functions.function import Function
from lib.util.functions.pair import Pair
from lib.util.number import Number
from lib.util.optional import Optional

if TYPE_CHECKING:
    from lib.serialization.decoder import Decoder


class DynamicLike[T](metaclass=ABCMeta):
    def __init__(self, ops: DynamicOps[T]) -> None:
        self.ops = ops

    def getOps(self):
        return self.ops

    @abstractmethod
    def asNumber(self) -> DataResult[Number]:
        pass

    @abstractmethod
    def asString(self) -> DataResult[str]:
        pass

    @abstractmethod
    def asBoolean(self) -> DataResult[bool]:
        pass

    @abstractmethod
    def get(self, key: str) -> OptionalDynamic[T]:
        pass

    @abstractmethod
    def getGeneric(self, key: T) -> DataResult[T]:
        pass

    @abstractmethod
    def getElement(self, key: str) -> DataResult[T]:
        pass

    @abstractmethod
    def getElementGeneric(self, key: T) -> DataResult[T]:
        pass

    @abstractmethod
    def decode[A](self, decoder: "Decoder[A]") -> DataResult[Pair[A, T]]:
        pass

    def emptyList(self) -> "Dynamic[T]":
        return Dynamic(self.ops, self.ops.emptyList())

    def emptyMap(self) -> "Dynamic[T]":
        return Dynamic(self.ops, self.ops.emptyMap())


class OptionalDynamic[T](DynamicLike[T]):
    def __init__(self, ops: DynamicOps[T], delegate: DataResult["Dynamic[T]"]) -> None:
        super().__init__(ops)
        self.delegate = delegate

    @dispatch
    def getDelegate(self) -> DataResult["Dynamic[T]"]:
        return self.delegate

    def result(self) -> Optional["Dynamic[T]"]:
        return self.delegate.result()

    def map[U](self, mapper: Function["Dynamic[T]", U]) -> DataResult[U]:
        return self.delegate.map(mapper)

    def flatMap[U](
        self, mapper: Function["Dynamic[T]", DataResult[U]]
    ) -> DataResult[U]:
        return self.delegate.flatMap(mapper)

    def asNumber(self) -> DataResult[Number]:
        return self.flatMap(super().asNumber)

    def asBoolean(self) -> DataResult[bool]:
        return self.flatMap(super().asBoolean)

    def asString(self) -> DataResult[str]:
        return self.flatMap(super().asString)

    @dispatch
    def get(self, key: str) -> "OptionalDynamic[T]":
        def _1(k: "Dynamic[T]"):
            return k.get(key).delegate

        return OptionalDynamic(self.ops, self.delegate.flatMap(_1))

    def getGeneric(self, key: T) -> DataResult[T]:
        def _1(v: "Dynamic[T]"):
            return v.getGeneric(key)

        return self.flatMap(_1)

    def getElement(self, key: str) -> DataResult[T]:
        def _1(v: "Dynamic[T]"):
            return v.getElement(key)

        return self.flatMap(_1)

    def getElementGeneric(self, key: T) -> DataResult[T]:
        def _1(v: "Dynamic[T]"):
            return v.getElementGeneric(key)

        return self.flatMap(_1)


class Dynamic[T](DynamicLike[T]):
    @dispatch
    def __init__(self, ops: DynamicOps[T]):
        super().__init__(ops)
        self.value = ops.empty()

    @dispatch
    def __init__(self, ops: DynamicOps[T], value: T | None) -> None:
        super().__init__(ops)
        self.value = ops.empty() if value is None else value

    def getValue(self) -> T:
        return self.value

    def map(self, function: Function[T, T]):
        return Dynamic(self.ops, function.apply(self.value))

    def castTyped[U](self, ops: DynamicOps[U]) -> Dynamic[U]:
        if self.ops != ops:
            raise TypeError("Dynamic type doesn't match")
        return self

    def cast[U](self, ops: DynamicOps[U]) -> U:
        return self.castTyped(ops).getValue()
