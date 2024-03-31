from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from lib.commands.util import Identifier

if TYPE_CHECKING:
    from lib.commands.entity import EntityType
    from lib.commands.registry.tag_key import TagKey

T = TypeVar("T")


class Registry(Generic[T]):
    content: dict[Identifier, T]

    def __init__(self) -> None:
        self.content: dict[Identifier, T] = dict()
        self.tagToEntryList: dict[TagKey[T], list[T]] = dict()

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

    def stream_tags(self):
        return self.tagToEntryList


class Registries():
    ENTITY_TYPE: Registry["EntityType"] = Registry()
