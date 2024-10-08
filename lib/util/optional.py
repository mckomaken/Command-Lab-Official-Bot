class Optional[T]():
    value: T

    def __init__(self, value: T) -> None:
        self.value = value

    @staticmethod
    def of[T](value: T) -> Optional[T]:
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