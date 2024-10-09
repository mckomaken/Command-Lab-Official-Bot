from abc import ABCMeta, abstractmethod
from lib.serialization.builder import RecordBuidler
from lib.serialization.compressor import CompressorHolder, KeyCompressor
from lib.serialization.data_result import DataResult
from lib.serialization.keyable import Keyable
from lib.serialization.lifecycle import Lifecycle
from lib.serialization.ops import DynamicOps
from lib.util.function import Function


class MapEncoder[A](Keyable, metaclass=ABCMeta):
    @abstractmethod
    def encode[T](self, input: A, ops: DynamicOps[T], prefix: RecordBuidler[T]) -> RecordBuidler[T]:
        pass

    def compressedBuilder[T](self, ops: DynamicOps[T]) -> RecordBuidler[T]:
        if ops.compressMaps():
            return
        return ops.mapBuilder()

    @abstractmethod
    def compressor[T](self, ops: DynamicOps[T]) -> KeyCompressor[T]:
        pass

    def comap[B](self, function: Function[B, A]) -> MapEncoder[B]:
        class _Impl(MapEncoder.Implementation[B]):
            def encode[T](_self, input: B, ops: DynamicOps[T], prefix: RecordBuidler[T]) -> RecordBuidler[T]:
                return self.encode(function.apply(input), ops, prefix)

            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def __str__(_self) -> str:
                return f"{self}[comapped]"

        return _Impl()

    def flatComap[B](self, function: Function[B, DataResult[A]]):
        class _Impl(MapEncoder.Implementation[B]):
            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def encode[T](_self, input: B, ops: DynamicOps[T], prefix: RecordBuidler[T]) -> RecordBuidler[T]:
                aResult = function.apply(input)
                builder = prefix.withErrorsFrom(aResult)
                return aResult.map(lambda r: self.encode(r, ops, builder)).result().orElse(builder)

            def __str__(_self) -> str:
                return f"{self}[flatComapped]"

        return _Impl()

    def encoder[B](self):
        class _Encoder(Encoder[A]):
            def encode[T](_self, input: A, ops: DynamicOps[T], prefix: T) -> DataResult[T]:
                return self.encode(input, ops, self.compressedBuilder(ops)).build(prefix)

            def __str__(_self) -> str:
                return f"{self}"

        return _Encoder()

    def withLifecycle(self, lifecycle: Lifecycle):
        class _Impl(MapEncoder.Implementation[A]):
            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def encode[T](_self, input: A, ops: DynamicOps[T], prefix: RecordBuidler[T]) -> RecordBuidler[T]:
                return self.encode(input, ops, prefix).setLifecycle(lifecycle)

        return _Impl()
    class Implementation[B](CompressorHolder, MapEncoder[A]):
        pass

class Encoder[A]():
    def encode[T](self, input: A, ops: DynamicOps[T], prefix: T) -> DataResult[T]:
        raise NotImplementedError()

    def encodeStart[T](self, ops: DynamicOps[T], input: A) -> DataResult[T]:
        return self.encode(input, ops, ops.empty())

    def comap[B](self, function: Function[B, A]):
