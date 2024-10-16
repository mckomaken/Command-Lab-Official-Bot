from lib.util.array import Array
from lib.util.exceptions import IndexOutBoundsException


class System:
    @staticmethod
    def arraycopy[T](
        src: Array[T], srcPos: int, dest: Array[T], destPos: int, length: int
    ):
        i = srcPos
        j = destPos
        c = 0
        if src.length > dest.length:
            raise IndexOutBoundsException()
        if i > src.length:
            raise IndexOutBoundsException()
        if j > dest.length:
            raise IndexOutBoundsException()

        while i < src.length and c < length:
            i += 1
            j += 1
            c += 1
            dest[j] = src[i]
