from abc import abstractmethod
from typing import Any, overload

from plum import dispatch

from lib.serialization.data_result import DataResult
from lib.serialization.encoder import Encoder
from lib.serialization.lifecycle import Lifecycle
from lib.serialization.ops import DynamicOps
from lib.util.functions.operator import UnaryOperator


class RecordBuidler[T]():
    @abstractmethod
    def getOps(self) -> DynamicOps[T]:
        pass

    @overload
    def add(self, key: T, value: T) -> RecordBuidler[T]: ...
    @overload
    def add(self, key: T, value: DataResult[T]) -> RecordBuidler[T]: ...
    @overload
    def add(self, key: DataResult[T], value: DataResult[T]) -> RecordBuidler[T]: ...
    @overload
    def add(self, key: str, value: T) -> RecordBuidler[T]: ...
    @overload
    def add(self, key: str, value: DataResult[T]) -> RecordBuidler[T]: ...
    @overload
    def add[E](self, key: str, value: E, encoder: Encoder[E]) -> RecordBuidler[T]: ...

    @dispatch
    @abstractmethod
    def add(self, key: T, value: T) -> RecordBuidler[T]:
        pass
    @dispatch
    @abstractmethod
    def add(self, key: T, value: DataResult[T]) -> RecordBuidler[T]:
        pass
    @dispatch
    @abstractmethod
    def add(self, key: DataResult[T], value: DataResult[T]) -> RecordBuidler[T]:
        pass

    @abstractmethod
    def withErrorsFrom(self, result: DataResult[Any]) -> RecordBuidler[T]:
        pass

    @abstractmethod
    def setLifecycle(self, lifecycle: Lifecycle) -> RecordBuidler[T]:
        pass

    @abstractmethod
    def mapError(self, onError: UnaryOperator[str]) -> RecordBuidler[T]:
        pass

    @overload
    def build(self, prefix: T) -> DataResult[T]: ...
    @overload
    def build(self, prefix: DataResult[T]) -> DataResult[T]: ...

    @dispatch
    @abstractmethod
    def build(self, prefix: T) -> DataResult[T]:
        pass

    @dispatch
    def build(self, prefix: DataResult[T]) -> DataResult[T]:
        return prefix.flatMap(self.build)

    @dispatch
    def add(self, key: str, value: T) -> RecordBuidler[T]:
        return self.add(self.getOps().createString(key), value)

    @dispatch
    def add(self, key: str, value: DataResult[T]) -> RecordBuidler[T]:
        return self.add(self.getOps().createString(key), value)

    @dispatch
    def add[E](self, key: str, value: E, encoder: Encoder[E]) -> RecordBuidler[T]:
        return self.add(key, encoder.encodeStart(self.getOps(), value))

    class AbstractBuilder[T, R](RecordBuidler[T]):
        def __init__(self, ops: DynamicOps[T]) -> None:
            self.ops = ops
            self.builder = DataResult.success(RecordBuidler.AbstractBuilder.initBuilder(), Lifecycle.STABLE)

        def getOps(self) -> DynamicOps[T]:
            return self.ops

        def initBuilder(self) -> R:
            raise NotImplementedError()

        def _build(self, builder: R, prefix: T) -> DataResult[T]:
            raise NotImplementedError()

        def build(self, prefix: T):
            result = self.builder.flatMap(lambda b: self._build(b, prefix))
            self.builder = DataResult.success(self.initBuilder(), Lifecycle.STABLE)
            return result

        def withErrorsFrom(self, result: DataResult[Any]) -> RecordBuidler[T]:
            def _flatMap(v: R):
                return result.map(lambda r: v)

            self.builder = self.builder.flatMap(_flatMap)
            return self

        def setLifecycle(self, lifecycle: Lifecycle) -> RecordBuidler[T]:
            self.builder = self.builder.setLifecycle(lifecycle)
            return self

        def mapError(self, onError: UnaryOperator[str]) -> RecordBuidler[T]:
            self.builder = self.builder.mapError(onError)
            return self