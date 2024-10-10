from abc import ABCMeta, abstractmethod
from typing import Any
from lib.serialization.keyable import Keyable
from lib.serialization.ops import DynamicOps


class Compressable(Keyable, metaclass=ABCMeta):
    @abstractmethod
    def compressor[T](self, ops: DynamicOps[T]) -> KeyCompressor[T]:
        pass


class CompressorHolder(Compressable):
    def __init__(self) -> None:
        self.compressors: dict[DynamicOps[Any], KeyCompressor[Any]] = dict()

    def compressor[T](self, ops: DynamicOps[T]) -> KeyCompressor[T]:
        v = self.compressors.get(ops, None)
        if v is None:
            newValue = KeyCompressor(ops, self.keys(ops))
            if newValue is not None:
                self.compressors[ops] = newValue
                return newValue
        return v


class KeyCompressor[T]:
    def __init__(self, ops: DynamicOps[T], keyList: list[T]) -> None:
        self.ops = ops
        self.compress: dict[T, int] = dict()
        self.compressString: dict[str, int] = dict()
        self.decompress: dict[int, T] = dict()

        for key in keyList:
            if key in self.compress:
                return
            next = len(self.compress)
            self.compress[key] = next

            def _k(k: str):
                self.compressString[k] = next

            ops.getStringValue(key).result().ifPresent(_k)
            self.decompress[next] = key

        self.size = len(self.compress)

    def decompressKey(self, key: int) -> T:
        return self.decompress.get(key)

    def compressKey(self, key: str) -> int:
        id = self.compressString.get(key)
        return self.compressT(self.ops.createString(key)) if id is None else id

    def compressT(self, key: T) -> int:
        return self.compress.get(key)

    def __len__(self):
        return self.size
