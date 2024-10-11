from __future__ import annotations
from abc import ABCMeta, abstractmethod
from lib.util.functions.consumer import Consumer
from lib.util.functions.function import Function
from lib.util.functions.iterator import Iterator
from lib.util.functions.predicate import Predicate


class BaseStream[T, S: "BaseStream[T, S]"](metaclass=ABCMeta):
    @abstractmethod
    def iterator(self) -> Iterator[T]:
        pass

    @abstractmethod
    def isParallel(self) -> bool:
        pass

    @abstractmethod
    def sequential(self) -> S:
        pass

    @abstractmethod
    def parallel(self) -> S:
        pass

    @abstractmethod
    def unordered(self) -> S:
        pass

    @abstractmethod
    def close(self):
        pass


class Stream[T](BaseStream[T, "Stream[T]"]):
    _internal: list[T]
    _i: int

    def __init__(self) -> None:
        self._internal = []
        self._i = 0

    def filter(self, predicate: Predicate[T]) -> Stream[T]:
        def _(obj: T):
            return predicate.test(obj)

        self._internal = list(filter(_, list(self._internal)))

    def map[R](self, mapper: Function[T, R]) -> Stream[R]:
        for i, e in enumerate(list(self._internal)):
            e[i] = mapper.apply(e)

    def forEach(self, action: Consumer[T]):
        for e in list(self._internal):
            action.accept(e)

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == len(self._internal):
            raise StopIteration()
        elm = self._internal[self._i]
        self._i += 1
        return elm

    def iterator(self) -> Iterator[T]:
        return Iterator(self._internal)
