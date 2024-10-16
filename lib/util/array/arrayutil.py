import copy

from lib.util.array import Array
from lib.util.spliterator import Spliterator, Spliterators


class Arrays:
    @staticmethod
    def copyOf[T](original: Array[T], newLength: int) -> Array[T]:
        newArray = Array[T](newLength)
        for i in range(original.length):
            newArray[i] = original[i]

        return newArray

    @staticmethod
    def spliterator[T](array: Array[T], startInclusive: int, endInclusive: int):
        return Spliterators.spliterator(
            array,
            startInclusive,
            endInclusive,
            Spliterator.ORDERED | Spliterator.IMMUTABLE,
        )
