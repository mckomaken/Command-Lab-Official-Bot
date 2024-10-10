from plum import dispatch

from lib.serialization.ops import DynamicOps
from lib.util.functions.function import Function


class DynamicLike[T]():
    def __init__(self, ops: DynamicOps[T]) -> None:
        self.ops = ops

    def getOps(self):
        return self.ops

class Dynamic[T](DynamicLike[T]):
    @dispatch
    def __init__(self, ops: DynamicOps[T]):
        super().__init__(ops)
        self.value = ops.empty()

    @dispatch
    def __init__(self, ops: DynamicOps[T], value: T | None) -> None:
        super().__init__(ops)
        self.value = ops.empty() if value is None else value

    def getValue(self) -> T:
        return self.value

    def map(self, function: Function[T, T]):
        return Dynamic(self.ops, function.apply(self.value))

    def castTyped[U](self, ops: DynamicOps[U]) -> Dynamic[U]:
        if self.ops != ops:
            return