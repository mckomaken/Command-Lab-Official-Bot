from lib.serialization.data_result import DataResult
from lib.serialization.dynamic import Dynamic
from lib.serialization.ops import DynamicOps
from lib.util.functions.pair import Pair


class Decoder[A]:
    def decode[T](self, ops: DynamicOps[T], input: T) -> DataResult[Pair[A, T]]:
        raise NotImplementedError()

    def parse[T](self, ops: DynamicOps[T], input: T) -> DataResult[A]:
        return self.decode(ops, input).map(lambda p: p.getLeft())

    def decode[T](self, input: Dynamic[T]) -> DataResult[Pair[A, T]]:
        return
