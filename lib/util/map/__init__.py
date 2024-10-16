from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from lib.util.collection import Collection
from lib.util.exceptions import ConcurrentModificationException, IllegalStateException
from lib.util.functions.consumer import BiConsumer
from lib.util.functions.function import BiFunction
from lib.util.set import Set


class Map[K, V](metaclass=ABCMeta):
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @abstractmethod
    def containsKey(self, key: Any) -> bool:
        pass

    @abstractmethod
    def containsValue(self, value: Any) -> bool:
        pass

    @abstractmethod
    def get(self, key: Any) -> V | None:
        pass

    @abstractmethod
    def put(self, key: K, value: V) -> V | None:
        pass

    @abstractmethod
    def remove(self, key: Any) -> V | None:
        pass

    @abstractmethod
    def putAll(self, m: Map[K, V]) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def keySet(self) -> Set[K]:
        pass

    @abstractmethod
    def values(self) -> Collection[V]:
        pass

    @abstractmethod
    def entrySet(self) -> Set[Map.Entry[K, V]]:
        pass

    class Entry[_K, _V](metaclass=ABCMeta):
        @abstractmethod
        def getKey(self) -> _K:
            pass

        @abstractmethod
        def getValue(self) -> _V:
            pass

        @abstractmethod
        def setValue(self, value: _V):
            pass

    def getOrDefault(self, key: Any, defaultValue: V) -> V:
        v = self.get(key)
        if v is not None or self.containsKey(key):
            return v
        else:
            return defaultValue

    def forEach(self, action: BiConsumer[K, V]):
        for entry in self.entrySet():
            try:
                k: K = entry.getKey()
                v = entry.getValue()
            except IllegalStateException as ise:
                raise ConcurrentModificationException(ise)
            else:
                action.accept(k, v)

    def replaceAll(self, action: BiFunction[K, V, V]):
        for entry in self.entrySet():
            try:
                k = entry.getKey()
                v = entry.getValue()
            except IllegalStateException as ise:
                raise ConcurrentModificationException(ise)
            else:
                v2 = action.apply(k, v)

            try:
                entry.setValue(v2)
            except IllegalStateException as ise:
                raise ConcurrentModificationException(ise)

    def putIfAbsent(self, key: K, value: V):
        v = self.get(key)
        if v is None:
            v = self.put(key, value)

        return v
