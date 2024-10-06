from typing import Any, Generic, Self, Type, TypeVar


T = TypeVar("T")
B = TypeVar("B", T)


class TypeFilter(Generic[B, T]):
    @staticmethod
    def instanceOf(cls: Type) -> Self:
        class _InstanceOf(TypeFilter):
            def downcast(self, obj: Any) -> Any:
                return obj if isinstance(obj, cls) else None

            def getBaseClass() -> Any:
                return cls

        return _InstanceOf()

    def downcast(self, obj: B) -> T:
        raise NotImplementedError()

    def getBaseClass(self) -> B:
        raise NotImplementedError()
