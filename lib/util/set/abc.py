from abc import ABCMeta
from typing import Any

from plum import dispatch

from lib.util.collection import AbstractImmutableCollection, Collection
from lib.util.set import Set


class AbstractImmutableSet[E](AbstractImmutableCollection[E], Set[E]):
    pass


class AbstractSet[E](Collection[E], Set[E], metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    def removeAll(self, c: Collection[Any]) -> bool:
        modified = False
        if self.size() > c.size():
            for e in c:
                modified |= self.remove(e)
        else:
            i = self.iterator()
            while i.hasNext():
                if c.contains(i.next()):
                    i.remove()
                    modified = True
        return modified


class HashSet[E](AbstractSet[E], Set[E]):
    @dispatch
    def __init__(self) -> None:
        from lib.util.map.hashmap import HashMap

        self.map = HashMap[E, Any]()
