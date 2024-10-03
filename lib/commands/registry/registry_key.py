from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

from lib.commands.util import Identifier

if TYPE_CHECKING:
    from lib.commands.entity import EntityType

INSTANCES: dict["RegistryKeyPair", "RegistryKey[Any]"] = dict()
T = TypeVar("T")


class RegistryKeys:
    ROOT: "RegistryKey" = Identifier("root")
    ENTITY_TYPE: "RegistryKey[EntityType]" = Identifier("entity_type")


class RegistryKey(Generic[T]):
    registry: Identifier
    value: Identifier

    @staticmethod
    def of(registry: Identifier, value: Identifier) -> Self:
        if RegistryKeyPair(registry, value) in INSTANCES.keys():
            pair = INSTANCES.get(RegistryKeyPair(registry, value))
        else:
            pair = RegistryKey(registry, value)
            INSTANCES[RegistryKeyPair(registry, value)] = pair

        return pair

    @staticmethod
    def ofRegistry(registry: Identifier):
        return RegistryKey(RegistryKeys.ROOT, registry)

    def __init__(self, registry: Identifier, value: Identifier) -> None:
        self.registry = registry
        self.value = value

    def __str__(self):
        return "ResourceKey[" + self.registry + " / " + self.value + "]"


class RegistryKeyPair:
    id: Identifier
    registry: Identifier

    def __init__(self, registry: Identifier, id: Identifier):
        self.id = id
        self.registry = registry
