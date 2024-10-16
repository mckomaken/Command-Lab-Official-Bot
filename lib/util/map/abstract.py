from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from lib.util.collection import AbstractCollection, Collection
from lib.util.exceptions import UnsupportedOperationException
from lib.util.iterator import Iterator
from lib.util.map import Map
from lib.util.set import Set
from lib.util.set.abc import AbstractSet
from lib.util.strutil import StringBuilder


class AbstractMap[K, V](Map[K, V], metaclass=ABCMeta):
    _keySet: Set[K]
    _values: Collection[V]

    def __init__(self) -> None:
        pass

    def size(self) -> int:
        return self.entrySet().size()

    def isEmpty(self) -> bool:
        return self.size() == 0

    def containsValue(self, value: Any) -> bool:
        i = self.entrySet().iterator()
        if value is None:
            while i.hasNext():
                e = i.next()
                if e.getValue() is None:
                    return True
        else:
            while i.hasNext():
                e = i.next()
                if value == e.getValue():
                    return True
        return False

    def containsKey(self, key: Any) -> bool:
        i = self.entrySet().iterator()
        if key is None:
            while i.hasNext():
                e = i.next()
                if e.getKey() is None:
                    return True
        else:
            while i.hasNext():
                e = i.next()
                if key == e.getKey():
                    return True
        return False

    def get(self, key: Any) -> V | None:
        i = self.entrySet().iterator()
        if key is None:
            while i.hasNext():
                e = i.next()
                if e.getKey() is None:
                    return e.getValue()
        else:
            while i.hasNext():
                e = i.next()
                if key == e.getKey():
                    return e.getValue()
        return None

    def put(self, key: K, value: V) -> V | None:
        raise UnsupportedOperationException()

    def remove(self, key: Any) -> V | None:
        i = self.entrySet().iterator()
        correctEntry = None
        if key is None:
            while correctEntry is None and i.hasNext():
                e = i.next()
                if e.getKey() is None:
                    correctEntry = e
        else:
            while correctEntry is None and i.hasNext():
                e = i.next()
                if key == e.getKey():
                    correctEntry = e

        oldValue = None
        if correctEntry is not None:
            oldValue = correctEntry.getValue()
            i.remove()
        return oldValue

    def putAll(self, m: Map[K, V]) -> None:
        for e in m.entrySet():
            self.put(e.getKey(), e.getValue())

    def clear(self) -> None:
        return self.entrySet().clear()

    def keySet(self) -> Set[K]:
        ks = self._keySet
        if ks is None:

            class _Impl(AbstractSet[K]):
                def iterator(_self) -> Iterator[K]:
                    return AbstractMap.KeyIterator(self)

                def size(_self) -> int:
                    return self.size()

                def isEmpty(_self) -> bool:
                    return self.isEmpty()

                def clear(_self) -> None:
                    return self.clear()

                def contains(_self, o: Any) -> bool:
                    return self.containsKey(o)

            ks = _Impl()

            self._keySet = ks

        return ks

    def values(self) -> Collection[V]:
        vals = self._values
        if vals is None:

            class _Impl(AbstractCollection[V]):
                def iterator(_self) -> Iterator[V]:
                    return AbstractMap.ValueIterator(self)

                def size(_self) -> int:
                    return self.size()

                def isEmpty(_self) -> bool:
                    return self.isEmpty()

                def clear(_self) -> None:
                    return self.clear()

                def contains(_self, o: Any) -> bool:
                    return self.containsValue(o)

            vals = _Impl()
            self._values = vals
        return vals

    @abstractmethod
    def entrySet(self) -> Set[Map.Entry[K, V]]:
        pass

    def __eq__(self, o: object) -> bool:
        if o == self:
            return True
        if not isinstance(o, Map):
            return False
        if o.size() != self.size():
            return False

        try:
            for e in self.entrySet():
                key = e.getKey()
                value = e.getValue()

                if value is None:
                    if not (o.get(key) is None and o.containsKey(key)):
                        return False
                else:
                    if value != o.get(key):
                        return False
        except Exception:
            return False

        return True

    def __str__(self) -> str:
        i = self.entrySet().iterator()
        if not i.hasNext():
            return "{}"

        sb = StringBuilder()
        sb.append("{")
        while True:
            e = i.next()
            key: K = e.getKey()
            value: V = e.getValue()
            sb.append("(this Map)" if key == self else str(key))
            sb.append("=")
            sb.append("(this Map)" if value == self else str(value))
            if not i.hasNext():
                return str(sb.append("}"))
            sb.append(", ")

    class KeyIterator(Iterator[K]):
        def __init__(self, i: Map) -> None:
            self.i = i.entrySet().iterator()

        def hasNext(self) -> bool:
            return self.i.hasNext()

        def next(self) -> K:
            return self.i.next().getKey()

        def remove(self) -> None:
            return self.i.remove()

    class ValueIterator(Iterator[V]):
        def __init__(self, i: Map) -> None:
            self.i = i.entrySet().iterator()

        def hasNext(self) -> bool:
            return self.i.hasNext()

        def next(self) -> K:
            return self.i.next().getValue()

        def remove(self) -> None:
            return self.i.remove()
