from lib.serialization.data_result import DataResult
from lib.serialization.keyable import Keyable
from lib.serialization.ops import DynamicOps


class MapEncoder[A](Keyable):
    

class Encoder[A]():
    def encode[T](self, input: A, ops: DynamicOps[T], prefix: T) -> DataResult[T]:
        raise NotImplementedError()

    def encodeStart[T](self, ops: DynamicOps[T], input: A) -> DataResult[T]:
        return self.encode(input, ops, ops.empty())
    
    def fieldOf()