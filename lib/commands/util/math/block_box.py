from typing import Iterable, Optional, Self

from lib.commands.util import MAX_INT, MIN_INT
from lib.commands.util.consumer import Consumer
from lib.commands.util.direction import Axis, Direction
from lib.commands.util.iterator import Iterator
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.util.math.vec3i import Vec3i
from lib.commands.util.mathhelper import MathHelper


class BlockBox:
    minX: int
    minY: int
    minZ: int
    maxX: int
    maxY: int
    maxZ: int

    @staticmethod
    def fromBlockPos(pos: BlockPos):
        BlockBox(pos.getX(), pos.getY(), pos.getZ(), pos.getX(), pos.getY(), pos.getZ())

    def __init__(self, minX: int, minY: int, minZ: int, maxX: int, maxY: int, maxZ: int):
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ
        if maxX < minX or maxY < minY or maxZ < minZ:
            print("Invalid bounding box data, inverted bounds for: " + self)
            self.minX = min(minX, maxX)
            self.minY = min(minY, maxY)
            self.minZ = min(minZ, maxZ)
            self.maxX = max(minX, maxX)
            self.maxY = max(minY, maxY)
            self.maxZ = max(minZ, maxZ)

    @staticmethod
    def create(first: Vec3i, second: Vec3i):
        return BlockBox(
            min(first.getX(), second.getX()),
            min(first.getY(), second.getY()),
            min(first.getZ(), second.getZ()),
            max(first.getX(), second.getX()),
            max(first.getY(), second.getY()),
            max(first.getZ(), second.getZ()),
        )

    @staticmethod
    def infinite():
        return BlockBox(MIN_INT, MIN_INT, MIN_INT, MAX_INT, MAX_INT, MAX_INT)

    @staticmethod
    def rotated(x, y, z, offsetX, offsetY, offsetZ, sizeX, sizeY, sizeZ, facing: Direction):
        match facing:
            case Direction.SOUTH, _:
                return BlockBox(
                    x + offsetX,
                    y + offsetY,
                    z + offsetZ,
                    x + sizeX - 1 + offsetX,
                    y + sizeY - 1 + offsetY,
                    z + sizeZ - 1 + offsetZ,
                )
            case Direction.NORTH:
                return BlockBox(
                    x + offsetX,
                    y + offsetY,
                    z - sizeZ + 1 + offsetZ,
                    x + sizeX - 1 + offsetX,
                    y + sizeY - 1 + offsetY,
                    z + offsetZ,
                )
            case Direction.WEST:
                return BlockBox(
                    x - sizeZ + 1 + offsetZ,
                    y + offsetY,
                    z + offsetX,
                    x + offsetZ,
                    y + sizeY - 1 + offsetY,
                    z + sizeX - 1 + offsetX,
                )
            case Direction.EAST:
                return BlockBox(
                    x + offsetZ,
                    y + offsetY,
                    z + offsetX,
                    x + sizeZ - 1 + offsetZ,
                    y + sizeY - 1 + offsetY,
                    z + sizeX - 1 + offsetX,
                )

    def intersects(self, other: "BlockBox") -> bool:
        return (
            self.maxX >= other.minX
            and self.minX <= other.maxX
            and self.maxZ >= other.minZ
            and self.minZ <= other.maxZ
            and self.maxY >= other.minY
            and self.minY <= other.maxY
        )

    def intersectsXZ(self, minX, minZ, maxX, maxZ):
        return self.maxX >= minX and self.minX <= maxX and self.maxZ >= minZ and self.minZ <= maxZ

    @staticmethod
    def encompassPositions(positions: list[BlockPos]) -> Optional["BlockBox"]:
        if len(positions) == 0:
            return None
        else:
            iterator = Iterator(positions)
            blockBox = BlockBox(iterator.next())
            iterator.forEachRemaining(blockBox.encompass)
            return blockBox

    @staticmethod
    def encompass(boxes: Iterable["BlockBox"]) -> Optional["BlockBox"]:
        iterator = Iterator(boxes)
        if not iterator.hasNext():
            return None
        else:
            blockBox = iterator.next()
            blockBox2 = BlockBox(
                blockBox.minX, blockBox.minY, blockBox.minZ, blockBox.maxX, blockBox.maxY, blockBox.maxZ
            )
            iterator.forEachRemaining(blockBox2.encompass)
            return blockBox2

    def encompass(self, pos: BlockPos):
        self.minX = min(self.minX, pos.getX())
        self.minY = min(self.minY, pos.getY())
        self.minZ = min(self.minZ, pos.getZ())
        self.maxX = max(self.maxX, pos.getX())
        self.maxY = max(self.maxY, pos.getY())
        self.maxZ = max(self.maxZ, pos.getZ())
        return self

    def move(self, dx: int, dy: int, dz: int):
        self.minX += dx
        self.minY += dy
        self.minZ += dz
        self.maxX += dx
        self.maxY += dy
        self.maxZ += dz
        return self

    def move(self, vec: Vec3i):
        return self.move(vec.getX(), vec.getY(), vec.getZ())

    def offset(self, x: int, y: int, z: int):
        return BlockBox(self.minX + x, self.minY + y, self.minZ + z, self.maxX + x, self.maxY + y, self.maxZ + z)

    def expand(self, offset: int):
        return self.expand(offset, offset, offset)

    def expand(self, x: int, y: int, z: int):
        return BlockBox(
            self.getMinX() - x,
            self.getMinY() - y,
            self.getMinZ() - z,
            self.getMaxX() + x,
            self.getMaxY() + y,
            self.getMaxZ() + z,
        )

    def contains(self, pos: Vec3i):
        return self.contains(pos.getX(), pos.getY(), pos.getZ())

    def contains(self, x: int, y: int, z: int):
        return (
            x >= self.minX
            and x <= self.maxX
            and z >= self.minZ
            and z <= self.maxZ
            and y >= self.minY
            and y <= self.maxY
        )

    def getDimensions(self):
        return Vec3i(self.maxX - self.minX, self.maxY - self.minY, self.maxZ - self.minZ)

    def getBlockCountX(self):
        return self.maxX - self.minX + 1

    def getBlockCountY(self):
        return self.maxY - self.minY + 1

    def getBlockCountZ(self):
        return self.maxZ - self.minZ + 1

    def getCenter(self):
        return BlockPos(
            self.minX + (self.maxX - self.minX + 1) / 2,
            self.minY + (self.maxY - self.minY + 1) / 2,
            self.minZ + (self.maxZ - self.minZ + 1) / 2,
        )

    def forEachVertex(self, consumer: Consumer[BlockPos]):
        mutable = BlockPos.Mutable()
        consumer.accept(mutable.set(self.maxX, self.maxY, self.maxZ))
        consumer.accept(mutable.set(self.minX, self.maxY, self.maxZ))
        consumer.accept(mutable.set(self.maxX, self.minY, self.maxZ))
        consumer.accept(mutable.set(self.minX, self.minY, self.maxZ))
        consumer.accept(mutable.set(self.maxX, self.maxY, self.minZ))
        consumer.accept(mutable.set(self.minX, self.maxY, self.minZ))
        consumer.accept(mutable.set(self.maxX, self.minY, self.minZ))
        consumer.accept(mutable.set(self.minX, self.minY, self.minZ))

    def __str__(self):
        return f"BlockBox[{self.maxX},{self.maxY},{self.maxZ}-{self.minX},{self.minY},{self.minZ}]"

    def __eq__(self, o: object):
        if self == o:
            return True
        elif not isinstance(o, BlockBox):
            return False
        else:
            return (
                self.minX == o.minX
                and self.minY == o.minY
                and self.minZ == o.minZ
                and self.maxX == o.maxX
                and self.maxY == o.maxY
                and self.maxZ == o.maxZ
            )

    def getMinX(self):
        return self.minX

    def getMinY(self):
        return self.minY

    def getMinZ(self):
        return self.minZ

    def getMaxX(self):
        return self.maxX

    def getMaxY(self):
        return self.maxY

    def getMaxZ(self):
        return self.maxZ
