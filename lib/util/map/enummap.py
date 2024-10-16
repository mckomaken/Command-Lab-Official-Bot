from enum import Enum
from typing import Any

from lib.util.array import Array
from lib.util.map.abstract import AbstractMap


class EnumMap[K: Enum, V](AbstractMap[K, V]):
    keyType: Enum
    keyUniverse: Array[K]
    vals: Array[Any]
    size: int

    @staticmethod
    def getKeyUniverse[_K](keyType: Enum) -> Array[_K]:
        return [n for n in keyType]

    def __init__(self, keyType: Enum) -> None:
        self.keyType = keyType
        self.keyUniverse = EnumMap.getKeyUniverse(keyType)
        self.vals = Array(self.keyUniverse.length)

    