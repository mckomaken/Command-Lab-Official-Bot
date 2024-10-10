from lib.commands.components import ComponentType


class NbtComponent(ComponentType[NbtCompound]):
    def __init__(self, compound: NbtCompound) -> None:
        super().__init__()
