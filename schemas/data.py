from typing import Optional

from pydantic import BaseModel, RootModel


class DataPathsEntry(BaseModel):
    attributes: Optional[str] = None
    blocks: Optional[str] = None
    blockCollisionShapes: Optional[str] = None
    biomes: Optional[str] = None
    effects: Optional[str] = None
    items: Optional[str] = None
    enchantments: Optional[str] = None
    recipes: Optional[str] = None
    instruments: Optional[str] = None
    materials: Optional[str] = None
    language: Optional[str] = None
    entities: Optional[str] = None
    protocol: Optional[str] = None
    windows: Optional[str] = None
    version: Optional[str] = None
    foods: Optional[str] = None
    particles: Optional[str] = None
    blockLoot: Optional[str] = None
    entityLoot: Optional[str] = None
    loginPacket: Optional[str] = None
    tints: Optional[str] = None
    mapIcons: Optional[str] = None
    commands: Optional[str] = None
    sounds: Optional[str] = None


class DataPaths(BaseModel):
    pc: dict[str, DataPathsEntry]
    bedrock: dict[str, DataPathsEntry]


class ItemEntry(BaseModel):
    id: int
    name: str
    displayName: str
    stackSize: int


class BlockEntryStates(BaseModel):
    name: str
    type: str
    num_values: int


class BlockEntry(BaseModel):
    id: int
    name: str
    displayName: str
    hardness: float
    resistance: float
    stackSize: int
    diggable: bool
    material: str
    transparent: bool
    emitLight: int
    filterLight: int
    defaultState: int
    minStateId: int
    maxStateId: int
    states: list[BlockEntryStates] = []
    harvestTools: Optional[dict[str, bool]] = None
    drops: list[int] = []
    boundingBox: Optional[str]


class Blocks(RootModel):
    root: list[BlockEntry]


class Items(RootModel):
    root: list[ItemEntry]


class CommandEntryJEBE(BaseModel):
    je: Optional[str] = None
    be: Optional[str] = None


class CommandEntry(BaseModel):
    is_diff: bool
    ver: CommandEntryJEBE
    desc: str
    exmp: CommandEntryJEBE
    options: CommandEntryJEBE
