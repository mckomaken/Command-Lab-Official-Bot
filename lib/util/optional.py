from lib.util.functions.consumer import Consumer
from lib.util.functions.function import Function


class Optional[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    @staticmethod
    def of[T](value: T) -> "Optional[T]":
        return Optional(value)

    @staticmethod
    def empty():
        return Optional(None)

    def get(self):
        if self.value is None:
            raise ValueError("No value present")
        return self.value

    def isPresent(self):
        return self.value is not None

    def isEmpty(self):
        return self.value is None

    def ifPresent(self, action: Consumer[T]):
        if self.value is not None:
            action.accept(self.value)

    def map[U](self, mapper: Function[T, U]):
        if self.isEmpty():
            return self.empty()
        else:
            return Optional.of(mapper.apply(self.value))

    def orElse(self, other: T):
        if self.value is not None:
            return self.value
        else:
            return other
