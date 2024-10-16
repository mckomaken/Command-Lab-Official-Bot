from __future__ import annotations

from abc import ABCMeta, abstractmethod

from plum import dispatch

from lib.serialization.compressor import CompressorHolder, KeyCompressor
from lib.serialization.data_result import DataResult
from lib.serialization.dynamic import Dynamic
from lib.serialization.keyable import Keyable
from lib.serialization.lifecycle import Lifecycle
from lib.serialization.maplike import MapLike
from lib.serialization.ops import DynamicOps
from lib.util.functions.function import Function
from lib.util.pair import Pair


class MapDecoder[A](Keyable, mataclass=ABCMeta):
    @abstractmethod
    def decode[T](self, ops: DynamicOps[T], input: MapLike[T]) -> DataResult[A]:
        pass

    def compressedDecode[T](self, ops: DynamicOps[T], input: T):
        if ops.compressMaps():
            inputList = ops.getList(input).result()
            if not inputList.isPresent():
                return DataResult.error(lambda: "Input is not a list")
            else:
                compressor = self.compressor(ops)
                entries = list()
                consumer = inputList.get()
                assert entries is not None
                consumer.accept(entries.append)

                class _Internal(MapLike[T]):
                    @dispatch
                    def get(self, key: T):
                        return entries[compressor.compress(key)]

                    @dispatch
                    def get(self, key: str) -> T:
                        return entries[compressor.compress(key)]

                    def entries(self) -> list[Pair[T, T]]:
                        result = list()
                        for i in range(len(entries)):
                            result.append(Pair.of(compressor.decompress(i), entries[i]))

                        def _(p: Pair[T, T]):
                            return p.getRight() is not None

                        return list(filter(_), result)

                return self.decode(ops, _Internal())
        else:
            return (
                ops.getMap(input)
                .setLifecycle(Lifecycle.STABLE)
                .flatMap(lambda mapx: self.decode(ops, mapx))
            )

    @abstractmethod
    def compressor[T](self, ops: DynamicOps[T]) -> KeyCompressor[T]:
        pass

    def decoder(self) -> Decoder[A]:
        class _Impl(Decoder[A]):
            def decode[T](
                _self, ops: DynamicOps[T], input: T
            ) -> DataResult[Pair[A, T]]:
                def _1(r: A):
                    return Pair.of(r, input)

                return self.compressedDecode(ops, input).map(_1)

            def __str__(_self) -> str:
                return str(self)

        return _Impl()

    def flatMap[B](self, function: Function[A, DataResult[B]]) -> MapDecoder[B]:
        class _Impl(MapDecoder.Implementation[B]):
            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def decode[T](_self, ops: DynamicOps[T], input: MapLike[T]):
                def _(b: A):
                    return function.apply(b).map(Function.identity())

                return self.decode(ops, input).flatMap(_)

            def __str__(self) -> str:
                return f"{str(self)}[flatMapped]"

        return _Impl()

    def map[B](self, function: Function[A, B]) -> MapDecoder[B]:
        class _Impl(MapDecoder.Implementation[B]):
            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def decode[T](_self, ops: DynamicOps[T], input: MapLike[T]):
                return self.decode(ops, input).map(function)

            def __str__(self) -> str:
                return f"{str(self)}[mapped]"

        return _Impl()

    def withLifecycle(self, lifecycle: Lifecycle):
        class _Impl(MapDecoder.Implementation[A]):
            def keys[T](_self, ops: DynamicOps[T]) -> list[T]:
                return self.keys(ops)

            def decode[T](_self, ops: DynamicOps[T], input: MapLike[T]):
                return self.decode(ops, input).setLifecycle(lifecycle)

            def __str__(self) -> str:
                return f"{str(self)}"

        return _Impl()

    class Implementation[_A](CompressorHolder, MapDecoder[_A]):
        def __init__(self) -> None:
            pass


class FieldDecoder[A](MapDecoder.Implementation[A]):
    name: str
    elementCodec: Decoder[A]

    def __init__(self, name: str, elementCodec: Decoder[A]) -> None:
        self.name = name
        self.elementCodec = elementCodec

    def decode[T](self, ops: DynamicOps[T], input: MapLike[T]) -> DataResult[A]:
        value = input.get(self.name)
        if value is None:
            return DataResult.error(lambda: f"No key {self.name} in {input}")
        return self.elementCodec.parse(ops, value)

    def keys[T](self, ops: DynamicOps[T]) -> list[T]:
        return


class Decoder[A]:
    def decode[T](self, ops: DynamicOps[T], input: T) -> DataResult[Pair[A, T]]:
        raise NotImplementedError()

    def parse[T](self, ops: DynamicOps[T], input: T) -> DataResult[A]:
        return self.decode(ops, input).map(lambda p: p.getLeft())

    def decodeDynamic[T](self, input: Dynamic[T]) -> DataResult[Pair[A, T]]:
        return self.decode(input.getOps(), input.getValue())

    def parseDynamic[T](self, input: Dynamic[T]) -> DataResult[A]:
        return self.decodeDynamic(input).map(lambda p: p.getLeft())
