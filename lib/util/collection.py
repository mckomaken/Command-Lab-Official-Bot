from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any

from lib.util.exceptions import UnsupportedOperationException
from lib.util.functions.predicate import Predicate
from lib.util.iterator import Iterable, Iterator
from lib.util.strutil import StringBuilder

if TYPE_CHECKING:
    from lib.util.spliterator import Spliterator
    from lib.util.stream import Stream


class Collection[E](Iterable[E], metaclass=ABCMeta):
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @abstractmethod
    def contains(self, o: Any) -> bool:
        pass

    @abstractmethod
    def iterator(self) -> Iterator[E]:
        pass

    @abstractmethod
    def add(self, e: E) -> bool:
        pass

    @abstractmethod
    def remove(self, o: Any) -> bool:
        pass

    @abstractmethod
    def containsAll(self, c: Collection[Any]) -> bool:
        pass

    @abstractmethod
    def addAll(self, c: Collection[E]) -> bool:
        pass

    @abstractmethod
    def removeAll(self, c: Collection[Any]) -> bool:
        pass

    def removeIf(self, filter: Predicate[E]) -> bool:
        removed = False
        each = self.iterator()
        while each.hasNext():
            if filter.test(each.next()):
                each.remove()
                removed = True

        return removed

    @abstractmethod
    def retainAll(self, c: Collection[Any]):
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    def spliterator(self) -> Spliterator[E]:
        from lib.util.spliterator import Spliterators

        return Spliterators.spliterator(self, 0)

    def stream(self) -> Stream[E]:
        from lib.util.stream import StreamSupport

        return StreamSupport.stream(self.spliterator(), False)

    def parallelStream(self) -> Stream[E]:
        from lib.util.stream import StreamSupport

        return StreamSupport.stream(self.spliterator(), True)

    def __iter__(self):
        return self.iterator()


class AbstractCollection[E](Collection[E]):
    def isEmpty(self) -> bool:
        return self.size() == 0

    def contains(self, o: Any) -> bool:
        it = self.iterator()
        if o is None:
            while it.hasNext():
                if it.next() is None:
                    return True
        else:
            while it.hasNext():
                if o == it.next():
                    return True
        return False

    def add(self, e: E):
        raise UnsupportedOperationException()

    def remove(self, o: Any) -> bool:
        it = self.iterator()
        if o is None:
            while it.hasNext():
                if it.next() is None:
                    it.remove()
                    return True
        else:
            while it.hasNext():
                if o == it.next():
                    it.remove()
                    return True

        return False

    def containsAll(self, c: Collection[Any]) -> bool:
        for e in c:
            if not self.contains(e):
                return False
        return True

    def addAll(self, c: Collection[E]) -> bool:
        modified = False
        for e in c:
            if self.add(e):
                modified = True
        return modified

    def removeAll(self, c: Collection[Any]) -> bool:
        modified = False
        it = self.iterator()
        while it.hasNext():
            if c.contains(it.next()):
                it.remove()
                modified = True
        return modified

    def retainAll(self, c: Collection[Any]):
        modified = False
        it = self.iterator()
        while it.hasNext():
            if not c.contains(it.next()):
                it.remove()
                modified = True
        return modified

    def clear(self) -> None:
        it = self.iterator()
        while it.hasNext():
            it.next()
            it.remove()

    def __str__(self) -> str:
        it = self.iterator()
        if not it.hasNext():
            return "[]"
        sb = StringBuilder()
        sb.append("[")
        while True:
            e = it.next()
            sb.append(str(e) if e != self else "(this Collection)")
            if not it.hasNext():
                return str(sb.append("]"))
            sb.append(", ")


class AbstractImmutableCollection[E](AbstractCollection[E]):
    def add(self, e: E):
        raise UnsupportedOperationException()

    def addAll(self, c: Collection[E]) -> bool:
        raise UnsupportedOperationException()

    def clear(self) -> None:
        raise UnsupportedOperationException()

    def remove(self, o: Any) -> bool:
        raise UnsupportedOperationException()

    def removeAll(self, c: Collection[Any]) -> bool:
        raise UnsupportedOperationException()

    def removeIf(self, filter: Predicate[E]) -> bool:
        raise UnsupportedOperationException()

    def retainAll(self, c: Collection[Any]):
        raise UnsupportedOperationException()
