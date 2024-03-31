from typing import Generic, TypeVar

from lib.commands.registry.registry_key import RegistryKey
from lib.commands.registry.tag_key import TagKey
from lib.commands.util import Identifier

from ..util.predicate import Predicate

T = TypeVar("T")


class RegistryEntry(Generic[T]):
    class Direct(Generic[T]):
        value: T

        def __init__(self, value: T) -> None:
            self.value = value

        def has_key_and_value(self):
            return True

        def matches_id(self, id: Identifier):
            return False

        def matches_key(self, key: RegistryKey[T]):
            return False

        def is_in(self, tag: TagKey[T]):
            return False

        def matches(self, predicate: Predicate[RegistryKey[T]]):
            return False

        def __str__(self) -> str:
            return f"Direct{self.value}"

    class Reference(Generic[T]):
        value: T

        def __init__(self, value: T) -> None:
            self.value = value

        def has_key_and_value(self):
            return True

        def matches_id(self, id: Identifier):
            return False

        def matches_key(self, key: RegistryKey[T]):
            return False

        def is_in(self, tag: TagKey[T]):
            return False

        def matches(self, predicate: Predicate[RegistryKey[T]]):
            return False

        def __str__(self) -> str:
            return f"Direct{self.value}"
