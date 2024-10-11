from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Any

from plum import dispatch

from lib.commands.nbt.scanner import NbtScanner
from lib.util.data import DataInput, DataOutput


class NbtSizeValidationException(Exception):
    pass


class NbtElement(metaclass=ABCMeta):
    @abstractmethod
    def write(self, output: DataOutput):
        pass

    @abstractmethod
    def getType(self) -> int:
        pass

    @abstractmethod
    def getNbtType(self) -> NbtType[Any]:
        pass

    @abstractmethod
    def copy(self) -> NbtElement:
        pass

    @abstractmethod
    def accept(self, vistor):
        pass

    @abstractmethod
    def doAccept(self, scanner: NbtScanner) -> NbtScanner.Result:
        pass

    def acceptScanner(self, visitor: NbtScanner):
        result = visitor.start(self.getNbtType())
        if result == NbtScanner.Result.CONTINUE:
            self.doAccept(visitor)


class NbtSizeTracker:
    def __init__(self, maxBytes: int, maxDepth: int) -> None:
        self.allocatedBytes = 0
        self.depth = 0
        self.maxBytes = maxBytes
        self.maxDepth = maxDepth

    @staticmethod
    def of(maxBytes: int) -> NbtSizeTracker:
        return NbtSizeTracker(maxBytes, 512)

    @dispatch
    def add(self, multipiler: int, bytes: int):
        self.add(multipiler * bytes)

    @dispatch
    def add(self, bytes: int):
        if (self.allocatedBytes + bytes) > self.maxBytes:
            raise NbtSizeValidationException(
                f"Tried to read NBT tag that was too big; tried to allocate: {self.allocatedBytes} + {bytes} +  bytes where max allowed: {self.maxBytes}"
            )
        else:
            self.allocatedBytes += bytes

    def pushStack(self):
        if self.depth >= self.maxDepth:
            raise NbtSizeValidationException(
                f"Tried to read NBT tag with too high complexity, depth > {self.maxDepth}"
            )
        else:
            self.depth += 1

    def popStack(self):
        if self.depth <= 0:
            raise NbtSizeValidationException(
                "NBT-Accounter tried to pop stack-depth at top-level"
            )
        else:
            self.depth -= 1

    def getAllocatedBytes(self):
        return self.allocatedBytes

    def getDepth(self):
        return self.depth


class NbtType[T: NbtElement](metaclass=ABCMeta):
    @abstractmethod
    def read(self, input: DataInput, tracker: NbtSizeTracker) -> T:
        pass

    @abstractmethod
    def doAccept(
        self, input: DataInput, visitor: NbtScanner, tracker: NbtSizeTracker
    ) -> NbtScanner.Result:
        pass

    def accept(self, input: DataInput, visitor: NbtScanner, tracker: NbtSizeTracker):
        match visitor.start(self):
            case NbtScanner.Result.CONTINUE:
                self.doAccept(input, visitor, tracker)
            case NbtScanner.Result.BREAK:
                self.skip(input, tracker)

    @abstractmethod
    def skip(self, input: DataInput, count: int, tracker: NbtSizeTracker):
        pass

    @abstractmethod
    def skip(self, input: DataInput, tracker: NbtSizeTracker):
        pass

    def isImmutable(self) -> bool:
        return False

    @abstractmethod
    def getCrashReportName(self) -> str:
        pass

    @abstractmethod
    def getCommandFeedbackName(self) -> str:
        pass
