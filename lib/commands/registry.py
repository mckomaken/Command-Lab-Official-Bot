from typing import Generic, Optional, TypeVar

from lib.commands.entity import EntityType
from lib.commands.util import Identifier


T = TypeVar("T")


class Registry(Generic[T]):
    content: dict[Identifier, T]

    def __init__(self) -> None:
        self.content = {}

    def get(self, id: Identifier) -> Optional[T]:
        return self.content[id]

    def get_ids(self) -> list[Identifier]:
        return self.content.keys()

    def get_or_throw(self, id: Identifier) -> T:
        if id in self.content:
            return self.content[id]
        else:
            raise ValueError("Missing key in " + str(T) + ": " + id)

    def register(self, element: T, id: Identifier):
        self.content[id] = element


class Registries():
    ENTITY_TYPE: Registry[EntityType] = Registry()
