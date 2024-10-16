from __future__ import annotations

from typing import Callable


class Predicate[T]:
    def __init__(self, cb: Callable[[T], bool]) -> None:
        self.condition = cb

    def test(self, v: T) -> bool:
        return self.condition(v)

    def Or(self, value: Predicate[T]) -> Predicate[T]:
        def _or(t: T) -> bool:
            return self.condition(t) or value.test(t)

        self.condition = _or
        return self

    def Negate(self) -> Predicate[T]:
        def _ne(t: T) -> bool:
            return not self.condition(t)

        self.condition = _ne
        return self

    def And(self, value: Predicate[T]) -> Predicate[T]:
        def _and(t: T) -> bool:
            return self.condition(t) and value.test(t)

        self.condition = _and
        return self
