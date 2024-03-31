from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Supplier(Generic[T]):
    def __init__(self, supplier: Callable[[], T]) -> None:
        self.supplier = supplier

    @classmethod
    def create(cls, supplier: T) -> "Supplier[T]":
        def _c():
            return supplier
        cls(_c)

    def get(self) -> T:
        return self.supplier()
