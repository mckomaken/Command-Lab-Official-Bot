from typing import Callable


class Supplier[T]:
    def __init__(self, cb: Callable[[], T]) -> None:
        self._cb = cb

    @classmethod
    def create(cls, supplier: T) -> "Supplier[T]":
        def _c():
            return supplier

        cls(_c)

    def get(self) -> T:
        return self._cb()
