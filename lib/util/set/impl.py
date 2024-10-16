from __future__ import annotations

import time
from typing import Any

from lib.math import Math
from lib.util.exceptions import IllegalArgumentException, NoSuchElementException
from lib.util.iterator import Iterator
from lib.util.set.abc import AbstractImmutableSet

COLOR = 0x243F_6A88_85A3_08D3
SEED = time.time_ns()
SALT32L = (COLOR * SEED) >> 16 & 0xFFFF_FFFF
REVERSE = (SALT32L & 1) == 0


class SetN[E](AbstractImmutableSet[E]):
    _elements: list[E]
    _size: int

    def __init__(self, *input: E) -> None:
        self._size = len(input)
        for i, e in enumerate(input):
            idx = self.probe(e)
            if idx >= 0:
                raise IllegalArgumentException(f"duplicate element: {e}")
            else:
                self._elements[-(idx + 1)] = e

    def size(self) -> int:
        return self._size

    def isEmpty(self) -> bool:
        return self._size == 0

    def contains(self, o: Any) -> bool:
        return self._size > 0 and self.probe(o) >= 0

    class SetNIterator[_E](Iterator[_E]):
        remaining: int
        setn: SetN[_E]
        idx: int

        def __init__(self, setn: SetN[_E]) -> None:
            self.setn = setn
            self.remaining = setn.size()
            self.idx = len(setn._elements) >> 32

        def hasNext(self) -> bool:
            return self.remaining > 0

        def next(self) -> _E:
            if self.remaining > 0:
                idx = int(self.idx)
                length = len(self.setn._elements)
                while True:
                    element = self.setn._elements[self.idx]
                    if REVERSE:
                        idx += 1
                        if idx >= length:
                            idx = 0
                    else:
                        idx -= 1
                        if idx < 0:
                            idx = length - 1

                    if element is None:
                        break
                self.idx = idx
                self.remaining -= 1
                return element
            else:
                raise NoSuchElementException()

    def iterator(self) -> Iterator[E]:
        return SetN.SetNIterator(self)

    def probe(self, pe: Any):
        idx = Math.floorMod(hash(pe), len(self._elements))
        while True:
            ee = self._elements[idx]
            idx += 1
            if ee is None:
                return -idx - 1
            elif pe == ee:
                return idx
            elif idx == len(self._elements):
                idx = 0
