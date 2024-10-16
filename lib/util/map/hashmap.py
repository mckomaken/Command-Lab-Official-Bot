from __future__ import annotations

from math import isnan

from plum import dispatch

from lib.util.exceptions import IllegalArgumentException
from lib.util.map import Map
from lib.util.map.abstract import AbstractMap
from lib.util.set import Set

MAXIMUM_CAPACITY = 1 << 30
DEFAULT_INITIAL_CAPACITY = 1 << 4
DEFAULT_LOAD_FACTOR = 0.75


class HashMap[K, V](AbstractMap[K, V]):
    table: Node[K, V]
    _entrySet: Set[Map.Entry[K, V]]
    size: int
    modCount: int
    threshold: int
    loadFactor: float

    class Node[_K, _V](Map.Entry[_K, _V]):
        def __init__(
            self, hash: int, key: _K, value: _V, next: HashMap.Node[_K, _V]
        ) -> None:
            self.hash = hash
            self.key = key
            self.value = value
            self.next = next

        def getKey(self) -> _K:
            return self.key

        def getValue(self) -> _V:
            return self.value

        def __str__(self) -> str:
            return f"{str(self.key)}={str(self.value)}"

        def __hash__(self) -> int:
            return hash(self.key) ^ hash(self.value)

        def setValue(self, value: _V):
            oldValue = self.value
            self.value = value
            return oldValue

    @staticmethod
    def tableSizeFor(cap: int) -> int:
        n = -1 >> (cap - 1)
        return 1 if n < 0 else (MAXIMUM_CAPACITY if n >= MAXIMUM_CAPACITY else n + 1)

    @dispatch
    def __init__(self, initialCapacity: int, loadFactor: float) -> None:
        if initialCapacity < 0:
            raise IllegalArgumentException(
                f"Illegal initial capacity: {initialCapacity}"
            )
        if initialCapacity > MAXIMUM_CAPACITY:
            initialCapacity = MAXIMUM_CAPACITY

        if loadFactor <= 0 or isnan(loadFactor):
            raise IllegalArgumentException(f"Illegal load factor: {loadFactor}")

        self.loadFactor = loadFactor
        self.threshold = HashMap.tableSizeFor(initialCapacity)

    @dispatch
    def __init__(self, initialCapacity: int):
        self.__init__(initialCapacity, DEFAULT_LOAD_FACTOR)

    @dispatch
    def __init__(self):
        self.loadFactor = DEFAULT_LOAD_FACTOR
