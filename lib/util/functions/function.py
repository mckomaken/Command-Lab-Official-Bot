from __future__ import annotations

from typing import Any, Callable


class Function[T1, R]:
    def __init__(self, cb: Callable[[T1], R]) -> None:
        self.cb = cb

    def apply(self, arg: T1) -> R:
        return self.cb(arg)

    @staticmethod
    def identity[_T]() -> Function[_T, _T]:
        def _(arg: _T) -> _T:
            return arg

        return Function(_)


class BiFunction[T1, T2, R]:
    def __init__(self, cb: Callable[[T1, T2], R]) -> None:
        self.cb = cb

    def apply(self, a: T1, b: T2) -> R:
        return self.cb(a, b)


class IntFunction[R]:
    def __init__(self, cb: Callable[[int], R]) -> None:
        self.cb = cb

    def apply(self, a: int) -> R:
        return self.cb(a)
