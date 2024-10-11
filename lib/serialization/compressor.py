from abc import ABCMeta, abstractmethod
from typing import Any

from plum import dispatch
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
        self._compress: dict[T, int] = dict()
        self._compressString: dict[str, int] = dict()
        self._decompress: dict[int, T] = dict()

        for key in keyList:
            if key in self._compress:
                return
            next = len(self._compress)
            self._compress[key] = next

            def _k(k: str):
                self._compressString[k] = next

            ops.getStringValue(key).result().ifPresent(_k)
            self._decompress[next] = key

        self.size = len(self._compress)

    def decompressKey(self, key: int) -> T:
        return self._decompress.get(key)

    @dispatch
    def compress(self, key: str) -> int:
        id = self._compressString.get(key)
        return self.compress(self.ops.createString(key)) if id is None else id

    @dispatch
    def compress(self, key: T) -> int:
        return self._compress.get(key)

    def decompress(self, key: int) -> T:
        return self._decompress.get(key)

    def __len__(self):
        return self.size
