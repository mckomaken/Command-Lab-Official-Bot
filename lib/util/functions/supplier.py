from typing import Callable

class Supplier[T](Callable[[], T]):
    @classmethod
    def create(cls, supplier: T) -> "Supplier[T]":
        def _c():
            return supplier

        cls(_c)

    def get(self) -> T:
        return self()
