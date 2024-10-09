from typing import Callable

class Predicate[T](Callable[[T], bool]):
    def test(self, v: T) -> bool:
        return self(v)

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
