from lib.commands.util.pair import Pair
from lib.util.stream import Stream


class MapLike[T]():
    def get(self, key: T) -> T:
        raise NotImplementedError()

    def entries(self) -> Stream[Pair[T, T]]:
        raise NotImplementedError()
