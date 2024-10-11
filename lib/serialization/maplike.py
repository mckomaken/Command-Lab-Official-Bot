from plum import dispatch
from lib.util.functions.pair import Pair


class MapLike[T]:
    @dispatch
    def get(self, key: T) -> T:
        raise NotImplementedError()

    @dispatch
    def get(self, key: str) -> T:
        raise NotImplementedError()

    def entries(self) -> list[Pair[T, T]]:
        raise NotImplementedError()
