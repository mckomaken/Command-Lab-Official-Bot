from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from lib.util.exceptions import UnsupportedOperationException
from lib.util.functions.consumer import Consumer

if TYPE_CHECKING:
    from lib.util.spliterator import Spliterator


class Iterable[T](metaclass=ABCMeta):
    @abstractmethod
    def iterator(self) -> Iterator[T]:
        pass

    def forEach(self, action: Consumer[T]) -> None:
        for t in self:
            action.accept(t)

    def spliterator(self) -> Spliterator[T]:
        from lib.util import Spliterators

        return Spliterators.spliteratorUnknownSize(self.iterator(), 0)

    def __iter__(self):
        return self.iterator()


class Iterator[E]:
    def __init__(self, obj: Iterable[E]) -> None:
        self.iterator = obj
        self.cursor = 0

    def hasNext(self) -> bool:
        return len(self.iterator) != self.cursor

    def next(self) -> E:
        elm = self.iterator[self.cursor]
        self.cursor += 1
        return elm

    def forEachRemaining(self, action: Consumer[E]):
        while self.hasNext():
            action.accept(self.next())

    def remove(self) -> None:
        raise UnsupportedOperationException("remove")

    def forEachRemaining(self, action: Consumer[E]):
        while self.hasNext():
            action.accept(self.next())

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration()
