from lib.commands.util.supplier import Supplier
from lib.serialization.ops import DynamicOps


class Keyable():
    def keys[T](self, ops: DynamicOps[T]) -> list[T]:
        raise NotImplementedError()

    @staticmethod
    def forStrings(keys: Supplier[list[str]]):
        class _Keyable(Keyable):
            def keys[T](self, ops: DynamicOps[T]) -> list[T]:
                for v in keys.get():
                    ops.createString(v)
                return keys.get()

        return _Keyable()