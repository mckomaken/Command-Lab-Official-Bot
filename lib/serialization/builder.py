from typing import Any

from plum import dispatch

from lib.serialization.data_result import DataResult
from lib.serialization.lifecycle import Lifecycle
from lib.serialization.ops import DynamicOps


class RecordBuidler[T]():
    def getOps(self) -> DynamicOps[T]:
        raise NotImplementedError()

    @dispatch
    def add(self, key: T, value: T) -> RecordBuidler[T]:
        raise NotImplementedError()

    @dispatch
    def add(self, key: T, value: DataResult[T]) -> RecordBuidler[T]:
        raise NotImplementedError()

    @dispatch
    def add(self, key: DataResult[T], value: DataResult[T]) -> RecordBuidler[T]:
        raise NotImplementedError()

    def withErrorsFrom(self, result: DataResult[Any]) -> RecordBuidler[T]:
        raise NotImplementedError()

    def setLifecycle(self, lifecycle: Lifecycle) -> RecordBuidler[T]:
        raise NotImplementedError()

    def mapError(self) -> RecordBuidler[T]:
        raise NotImplementedError()

    def build(self, prefix: T) -> DataResult[T]:
        raise NotImplementedError()