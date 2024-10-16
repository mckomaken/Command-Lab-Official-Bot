from __future__ import annotations

from abc import ABCMeta

from lib.util.collection import Collection
from lib.util.spliterator import Spliterator, Spliterators


class Set[E](Collection[E], metaclass=ABCMeta):
    def spliterator(self) -> Spliterator[E]:
        return Spliterators.spliterator(self, Spliterator.DISTINCT)

    @staticmethod
    def of[_E]() -> Set[_E]:
        from lib.util.set.impl import SetN

        return SetN[_E]()
