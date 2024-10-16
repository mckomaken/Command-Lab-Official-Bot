from __future__ import annotations

from typing import Callable


class Supplier[T]:
    def __init__(self, cb: Callable[[], T]) -> None:
        self._cb = cb

    @staticmethod
    def create[_T](supplier: _T) -> Supplier[_T]:
        def _c() -> _T:
            return supplier

        return Supplier(_c)

    def get(self) -> T:
        return self._cb()
