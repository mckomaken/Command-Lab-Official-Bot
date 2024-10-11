from typing import Callable


class Function[T1, R](Callable[[T1], R]):
    def apply(self, arg: T1) -> R:
        return self(arg)

    @staticmethod
    def identity[_T]() -> Function[_T, _T]:
        def _(arg: _T):
            return arg

        return _


class BiFunction[T1, T2, R](Callable[[T1, T2], R]):
    def apply(self, a: T1, b: T2) -> R:
        return self(a, b)
