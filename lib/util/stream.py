from lib.commands.util.predicate import Predicate
from lib.util.function import Function


class Stream[T]:
    def filter(self, predicate: Predicate[T]) -> Stream[T]:
        raise NotImplementedError()

    def map[R](self, mapper: Function[T, R]) -> Stream[R]:
        raise NotImplementedError()
