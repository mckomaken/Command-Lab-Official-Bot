from lib.util.functions.function import Function
from lib.util.functions.predicate import Predicate


class Stream[T]:
    def filter(self, predicate: Predicate[T]) -> "Stream[T]":
        raise NotImplementedError()

    def map[R](self, mapper: Function[T, R]) -> "Stream[R]":
        raise NotImplementedError()
