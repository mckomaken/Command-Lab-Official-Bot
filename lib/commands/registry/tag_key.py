from typing import Generic, TypeVar

from lib.commands.registry.interner import Interner
from lib.commands.registry.registry import Registry
from lib.commands.registry.registry_key import RegistryKey
from lib.commands.util import Identifier

T = TypeVar("T")
INTERNER = None


class TagKey(Generic[T]):
    registry: RegistryKey[Registry[T]]
    id: Identifier

    def __init__(self, registry: RegistryKey[Registry[T]], id: Identifier) -> None:
        self.registry = registry
        self.id = id

    @staticmethod
    def of(registry: RegistryKey[Registry[T]], id: Identifier):
        return INTERNER.intern(TagKey(registry, id))

    def isOf(self, ref: RegistryKey[Registry[T]]) -> bool:
        return self.registry == ref

    def __str__(self) -> str:
        return f"TagKey[{self.registry.value}/{self.id}]"


INTERNER = Interner[TagKey[T]]()
