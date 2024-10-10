from __future__ import annotations
from abc import ABCMeta, abstractmethod


class NbtElement(metaclass=ABCMeta):
    @abstractmethod
    def write(self, output):
        pass

    @abstractmethod
    def getType(self) -> int:
        pass

    @abstractmethod
    def copy(self) -> NbtElement:
        pass
