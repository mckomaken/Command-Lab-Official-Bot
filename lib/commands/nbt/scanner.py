from __future__ import annotations
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Any

from lib.commands.nbt import NbtType


class NbtScanner(metaclass=ABCMeta):
    @abstractmethod
    def start(rootType: NbtType[Any]) -> Result:
        pass

    class Result(Enum):
        CONTINUE = auto()
        BREAK = auto()
        HALT = auto()
