from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Consumer(Generic[T]):
    def __init__(self, cb: Callable[[T], None]):
        self.cb = cb

    def accept(self, v: T):
        self.cb(v)
