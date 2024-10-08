from ast import Call
from typing import Callable, TypeVar


class Function[T1, R](Callable[[T1], R]):
    def apply(self, arg: T1) -> R:
        return self(arg)

class BiFunction[T1, T2, R](Callable[[T1, T2], R]):
    def apply(self, a: T1, b: T2) -> R:
        return self(a, b)