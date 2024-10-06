import math
from typing import Self, overload

from lib.commands.util.direction import Axis, Direction
from lib.commands.util.math.block_rotation import BlockRotation
from lib.commands.util.math.vec3i import Vec3i
from lib.commands.util.mathhelper import MathHelper


class BlockPos(Vec3i):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)

    @staticmethod
    def ofFloored(x: float, y: float, z: float):
        return BlockPos(math.floor(x), math.floor(y), math.floor(z))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def add(self, vec3i: Vec3i) -> "BlockPos":
        return self.add(vec3i.getX(), vec3i.getY(), vec3i.getZ())

    def subtract(self, vec3i: Vec3i) -> "BlockPos":
        return super().add(-vec3i.getX(), -vec3i.getY(), -vec3i.getZ())

    def multiply(self, i: int):
        if i == 1:
            return self
        else:
            return BlockPos(self.getX() * i, self.getY() * i, self.getZ() * i)

    def up(self):
        return self.offset(Direction.UP)

    def up(self, distance: int):
        return self.offset(Direction.UP, distance)

    def down(self):
        return self.offset(Direction.DOWN)

    def down(self, i: int):
        return self.offset(Direction.DOWN, i)

    def north(self):
        return self.offset(Direction.NORTH)

    def north(self, distance: int):
        return self.offset(Direction.NORTH, distance)

    def south(self):
        return self.offset(Direction.SOUTH)

    def south(self, distance: int):
        return self.offset(Direction.SOUTH, distance)

    def west(self):
        return self.offset(Direction.WEST)

    def west(self, distance: int):
        return self.offset(Direction.WEST, distance)

    def east(self):
        return self.offset(Direction.EAST)

    def east(self, distance: int):
        return self.offset(Direction.EAST, distance)

    def offset(self, direction: Direction):
        return BlockPos(
            self.getX() + direction.getOffsetX(),
            self.getY() + direction.getOffsetY(),
            self.getZ() + direction.getOffsetZ(),
        )

    def offset(self, direction: Direction, i: int):
        if i == 0:
            return self
        return BlockPos(
            self.getX() + direction.getOffsetX() * i,
            self.getY() + direction.getOffsetY() * i,
            self.getZ() + direction.getOffsetZ() * i,
        )

    def offset(self, axis: Axis, i: int):
        if i == 0:
            return self
        else:
            j = i if axis == Axis.X else 0
            k = i if axis == Axis.Y else 0
            l = i if axis == Axis.Z else 0
            return BlockPos(self.getX() + j, self.getY() + k, self.getZ() + l)

    def rotate(self, rotation: BlockRotation):
        match rotation:
            case BlockRotation.NONE, _:
                return self
            case BlockRotation.CLOCKWISE_90:
                return BlockPos(-self.getZ(), self.getY(), self.getX())
            case BlockRotation.CLOCKWISE_180:
                return BlockPos(-self.getX(), self.getY(), -self.getZ())
            case BlockRotation.COUNTERCLOCKWISE_90:
                return BlockPos(self.getZ(), self.getY(), -self.getX())

    def crossProduct(self, pos: Vec3i):
        return BlockPos(
            self.getY() * pos.getZ() - self.getZ() * pos.getY(),
            self.getZ() * pos.getX() - self.getX() * pos.getZ(),
            self.getX() * pos.getY() - self.getY() * pos.getX(),
        )

    def withY(self, y: int):
        return BlockPos(self.getX(), y, self.getZ())

    def toImmutable(self):
        return self


class MutableBlockPos(BlockPos):
    def __init__(self):
        super().__init__(0, 0, 0)

    def add(self, i: int, j: int, k: int):
        return self.add(i, j, k).toImmutable()

    def multiply(self, i):
        return self.multiply(i).toImmutable()

    def offset(self, direction: Direction, i: int):
        return self.offset(direction, i).toImmutable()

    def offset(self, axis: Axis, i: int):
        return self.offset(axis, i).toImmutable()

    def rotate(self, rotation: BlockRotation):
        return self.rotate(rotation).toImmutable()

    def set(self, x: int, y: int, z: int):
        self.setX(x)
        self.setY(y)
        self.setZ(z)
        return self

    def set(self, x: float, y: float, z: float):
        return self.set(MathHelper.floor(x), MathHelper.floor(y), MathHelper.floor(z))

    def set(self, pos: Vec3i):
        return self.set(pos.getX(), pos.getY(), pos.getZ())

    def set(self, pos: int):
        return self.set(unpackLongX(pos), unpackLongY(pos), unpackLongZ(pos))

    def set(self, axis: Axis, x: int, y: int, z: int):
        return self.set(axis.choose(x, y, z, Axis.X), axis.choose(x, y, z, Axis.Y), axis.choose(x, y, z, Axis.Z))

    def set(self, pos: Vec3i, direction: Direction):
        return self.set(
            pos.getX() + direction.getOffsetX(),
            pos.getY() + direction.getOffsetY(),
            pos.getZ() + direction.getOffsetZ(),
        )

    def set(self, pos: Vec3i, x: int, y: int, z: int):
        return self.set(pos.getX() + x, pos.getY() + y, pos.getZ() + z)

    def set(self, vec1: Vec3i, vec2: Vec3i):
        return self.set(vec1.getX() + vec2.getX(), vec1.getY() + vec2.getY(), vec1.getZ() + vec2.getZ())

    def move(self, direction: Direction):
        return self.move(direction, 1)

    def move(self, direction: Direction, distance: int):
        return self.set(
            self.getX() + direction.getOffsetX() * distance,
            self.getY() + direction.getOffsetY() * distance,
            self.getZ() + direction.getOffsetZ() * distance,
        )

    def move(self, dx: int, dy: int, dz: int):
        return self.set(self.getX() + dx, self.getY() + dy, self.getZ() + dz)

    def move(self, vec: Vec3i):
        return self.set(self.getX() + vec.getX(), self.getY() + vec.getY(), self.getZ() + vec.getZ())

    def clamp(self, axis: Axis, min: int, max: int):
        match axis:
            case Axis.X:
                return self.set(MathHelper.clamp(self.getX(), min, max), self.getY(), self.getZ())
            case Axis.Y:
                return self.set(self.getX(), MathHelper.clamp(self.getY(), min, max), self.getZ())
            case Axis.Z:
                return self.set(self.getX(), self.getY(), MathHelper.clamp(self.getZ(), min, max))

    def setX(self, i: int):
        self.setX(i)
        return self

    def setY(self, i: int):
        self.setY(i)
        return self

    def setZ(self, i: int):
        self.setZ(i)
        return self

    def toImmutable(self) -> BlockPos:
        return BlockPos(self)
