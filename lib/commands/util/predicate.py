from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Predicate(Generic[T]):
    def __init__(self, condition: Callable[[T], bool]) -> None:
        self.condition = condition

    def test(self, v: T) -> bool:
        return self.condition(v)

    def Or(self, value: "Predicate") -> "Predicate":
        def _or(t) -> bool:
            return self.condition(t) or value(t)
        self.condition = _or

    def Negate(self) -> "Predicate":
        def _ne(t) -> bool:
            return not self.condition(t)
        self.condition = _ne

    def And(self, value: "Predicate"):
        def _and(t) -> bool:
            return self.condition(t) and value(t)
        self.condition = _and
