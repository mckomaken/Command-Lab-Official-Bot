from typing import Iterable

from lib.util.functions.consumer import Consumer


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
