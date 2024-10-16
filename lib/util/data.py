from abc import ABCMeta, abstractmethod

from fixedint import Int8, Int16, Int64, UInt8, UInt16


class DataInput(metaclass=ABCMeta):
    @abstractmethod
    def readBoolean(self) -> bool:
        pass

    @abstractmethod
    def skipBytes(self, n: int) -> int:
        pass

    @abstractmethod
    def readByte(self) -> Int8:
        pass

    @abstractmethod
    def readUnsignedByte(self) -> UInt8:
        pass

    @abstractmethod
    def readShort(self) -> Int16:
        pass

    @abstractmethod
    def readUnsignedShort(self) -> UInt16:
        pass

    @abstractmethod
    def readInt(self) -> int:
        pass

    @abstractmethod
    def readLong(self) -> Int64:
        pass

    @abstractmethod
    def readFloat(self) -> float:
        pass

    @abstractmethod
    def readDouble(self) -> float:
        pass

    @abstractmethod
    def readLine(self) -> str:
        pass


class DataOutput(metaclass=ABCMeta):
    @abstractmethod
    def writeBoolean(self, v: bool):
        pass

    @abstractmethod
    def writeByte(self, v: Int8):
        pass

    @abstractmethod
    def writeUnsignedByte(self, v: UInt8):
        pass

    @abstractmethod
    def writeShort(self, v: Int16):
        pass

    @abstractmethod
    def writeUnsignedShort(self, v: UInt16):
        pass

    @abstractmethod
    def writeInt(self, v: int):
        pass

    @abstractmethod
    def writeLong(self, v: Int64):
        pass

    @abstractmethod
    def writeFloat(self, v: float):
        pass

    @abstractmethod
    def writeDouble(self, v: float):
        pass

    @abstractmethod
    def writeBytes(self, v: str):
        pass

    @abstractmethod
    def writeChars(self, v: str):
        pass
