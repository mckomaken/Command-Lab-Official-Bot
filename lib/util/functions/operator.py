from lib.util.function import Function


class UnaryOperator[T](Function[T, T]):
    @staticmethod
    def identity[_T]() -> UnaryOperator[_T]:
        return lambda t: t