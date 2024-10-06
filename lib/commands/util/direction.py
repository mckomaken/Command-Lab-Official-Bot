import math
from enum import Enum
from random import Random
from tkinter import NO
from typing import Optional, Self
from xml.dom.minidom import Entity

from lib.commands.util import Util
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.util.math.vec3i import Vec3i
from lib.commands.util.mathhelper import MathHelper
from lib.math.vector.quaternion import Quaternion


class Axis(Enum):
    X = (0, "x")
    Y = (1, "y")
    Z = (2, "z")

    def __init__(self, ordinal: int, literal: str) -> None:
        self.literal = literal
        self._ordinal = ordinal

    def choose(self, x: float, y: float, z: float):
        match self.literal:
            case "x":
                return x
            case "y":
                return y
            case "z":
                return z

    def isVertical(self):
        return self == Axis.Y

    def isHorizontal(self):
        return self == Axis.X or self == Axis.Z

    def ordinal(self):
        return self._ordinal

    @staticmethod
    def values():
        return [v for v in Axis]


class AxisDirection(Enum):
    POSITIVE = (1, "Towards positive")
    NEGATIVE = (-1, "Towards negative")

    def __init__(self, offset: int, description: str):
        self.offest = offset
        self.description = description

    def getOpposite(self):
        return AxisDirection.POSITIVE if self == AxisDirection.NEGATIVE else AxisDirection.NEGATIVE

    def __str__(self) -> str:
        return self.description


class Direction(Enum):
    DOWN = (0, 1, -1, "down", AxisDirection.NEGATIVE, Axis.Y, Vec3i(0, -1, 0))
    UP = (1, 0, -1, "up", AxisDirection.POSITIVE, Axis.Y, Vec3i(0, 1, 0))
    NORTH = (2, 3, 2, "north", AxisDirection.NEGATIVE, Axis.Z, Vec3i(0, 0, -1))
    SOUTH = (3, 2, 0, "south", AxisDirection.POSITIVE, Axis.Z, Vec3i(0, 0, 1))
    WEST = (4, 5, 1, "west", AxisDirection.NEGATIVE, Axis.X, Vec3i(-1, 0, 0))
    EAST = (5, 4, 3, "east", AxisDirection.POSITIVE, Axis.X, Vec3i(1, 0, 0))

    @staticmethod
    @property
    def ALL():
        return [v for v in Direction]

    @staticmethod
    @property
    def VALUES():
        return sorted(Direction.ALL)

    @staticmethod
    @property
    def HORIZONTAL():
        return [v for v in Direction.ALL if v.getAxis().isHorizontal()]

    def ordinal(self):
        return self.id

    def __init__(
        self,
        id: int,
        idOpposite: int,
        idHorizontal: int,
        name: str,
        direction: AxisDirection,
        axis: Axis,
        vector: Vec3d,
    ) -> Self:
        self.id = id
        self.idOpposite = idOpposite
        self.idHorizontal = idHorizontal
        self._name = name
        self.axis = axis
        self.direction = direction
        self.vector = vector

    def getRotationQuaternion(self):
        match self._name:
            case 0:
                result = (Quaternion()).rotationX(3.1415927)
            case 1:
                result = Quaternion()
            case 2:
                result = (Quaternion()).rotationXYZ(1.5707964, 0.0, 3.1415927)
            case 3:
                result = (Quaternion()).rotationX(1.5707964)
            case 4:
                result = (Quaternion()).rotationXYZ(1.5707964, 0.0, 1.5707964)
            case 5:
                result = (Quaternion()).rotationXYZ(1.5707964, 0.0, -1.5707964)
            case _:
                raise ValueError()

        return result

    def getId(self):
        return self.id

    def getHorizontal(self):
        return self.idHorizontal

    def getDirection(self):
        return self.direction

    @staticmethod
    def getLookDirectionForAxis(entity: Entity, axis: Axis) -> Self:
        match axis.ordinal():
            case 0:
                return Direction.EAST if Direction.EAST.pointsTo(entity.getYaw(1.0)) else Direction.WEST
            case 1:
                return Direction.UP if entity.getPitch(1.0) < 0.0 else Direction.DOWN
            case 2:
                return Direction.SOUTH if Direction.SOUTH.pointsTo(entity.getYaw(1.0)) else Direction.NORTH
            case _:
                raise ValueError()

    def getOpposite(self):
        return Direction[self.idOpposite]

    def rotateClockwise(self, axis: Axis):
        match axis.ordinal():
            case 0:
                return self.rotateXClockwise() if self != Direction.WEST and self != Direction.EAST else self
            case 1:
                return self.rotateYClockwise() if self != Direction.UP and self != Direction.DOWN else self
            case 2:
                return self.rotateZClockwise() if self != Direction.NORTH and self != Direction.SOUTH else self

    def rotateCounterclockwise(self, axis: Axis):
        match axis.ordinal():
            case 0:
                return self.rotateXCounterclockwise() if self != Direction.WEST and self != Direction.EAST else self
            case 1:
                return self.rotateYCounterclockwise() if self != Direction.UP and self != Direction.DOWN else self
            case 2:
                return self.rotateZCounterclockwise() if self != Direction.NORTH and self != Direction.SOUTH else self

    def rotateYClockwise(self):
        match self.ordinal():
            case 2:
                return Direction.EAST
            case 3:
                return Direction.WEST
            case 4:
                return Direction.NORTH
            case 5:
                return Direction.SOUTH
            case _:
                raise ValueError(f"Unable to get Y-rotated facing of {self}")

    def rotateXClockwise(self):
        match self.ordinal():
            case 0:
                return Direction.SOUTH
            case 1:
                return Direction.NORTH
            case 2:
                return Direction.DOWN
            case 3:
                return Direction.UP
            case _:
                raise ValueError(f"Unable to get X-rotated facing of {self}")

    def rotateXCounterclockwise(self):
        match self.ordinal():
            case 0:
                return Direction.NORTH
            case 1:
                return Direction.SOUTH
            case 2:
                return Direction.UP
            case 3:
                return Direction.DOWN
            case _:
                raise ValueError(f"Unable to get X-rotated facing of {self}")

    def rotateZClockwise(self):
        match self.ordinal():
            case 0:
                return Direction.WEST
            case 1:
                return Direction.EAST
            case 2, 3, _:
                raise ValueError(f"Unable to get Z-rotated facing of {self}")
            case 4:
                return Direction.UP
            case 5:
                return Direction.DOWN

    def rotateZCounterclockwise(self):
        match self.ordinal():
            case 0:
                return Direction.EAST
            case 1:
                return Direction.WEST
            case 2, 3, _:
                return ValueError(f"Unable to get Z-rotated facing of {self}")
            case 4:
                return Direction.DOWN
            case 5:
                return Direction.UP

    def rotateYCounterclockwise(self):
        match self.ordinal():
            case 2:
                return Direction.WEST
            case 3:
                return Direction.EAST
            case 4:
                return Direction.SOUTH
            case 5:
                return Direction.NORTH
            case _:
                raise ValueError(f"Unable to get CCW facing of {self}")

    def getOffsetX(self):
        return self.vector.getX()

    def getOffsetY(self):
        return self.vector.getY()

    def getOffsetZ(self):
        return self.vector.getZ()

    def getUnitVector(self):
        return Vec3d(self.getOffsetX(), self.getOffsetY(), self.getOffsetZ())

    def getName(self):
        return self.name

    def getAxis(self):
        return self.axis

    @staticmethod
    def byId(id: int):
        return Direction.VALUES[abs(id % len(Direction.VALUES))]

    @staticmethod
    def fromHorizontal(value):
        return Direction.HORIZONTAL[abs(value % len(Direction.HORIZONTAL))]

    @staticmethod
    def fromVector(x: int, y: int, z: int) -> Optional["Direction"]:
        if x == 0:
            if y == 0:
                if z > 0:
                    return Direction.SOUTH

                if z < 0:
                    return Direction.NORTH

            elif z == 0:
                if y > 0:
                    return Direction.UP

                return Direction.DOWN

        elif y == 0 and z == 0:
            if x > 0:
                return Direction.EAST

            return Direction.WEST

        return None

    @staticmethod
    def fromRotation(rotation: float):
        return Direction.fromHorizontal(MathHelper.floor(rotation / 90.0 + 0.5) & 3)

    @staticmethod
    def fromAxis(axis: Axis, direction: AxisDirection):
        match axis.ordinal():
            case 0:
                return Direction.EAST if direction == AxisDirection.POSITIVE else Direction.WEST
            case 1:
                return Direction.UP if direction == AxisDirection.POSITIVE else Direction.DOWN
            case 2:
                return Direction.SOUTH if direction == AxisDirection.POSITIVE else Direction.NORTH
            case _:
                raise ValueError()

    def asRotation(self) -> float:
        return (self.idHorizontal & 3) * 90

    @staticmethod
    def random(random: Random):
        return Util.getRandom(Direction.ALL, random)

    @staticmethod
    def getFacing(x: float, y: float, z: float):
        direction = Direction.NORTH
        f = -math.inf

        for direction2 in Direction:
            g = x * direction2.vector.getX() + y * direction2.vector.getY() + z * direction2.vector.getZ()
            if g > f:
                f = g
                direction = direction2

        return direction

    @staticmethod
    def getFacing(vec: Vec3d):
        return Direction.getFacing(vec.x, vec.y, vec.z)

    def __str__(self) -> str:
        return self.name

    def get(direction: AxisDirection, axis: Axis):
        for direction2 in Direction:
            if direction2.getDirection() == direction and direction2.getAxis() == axis:
                return direction2

        raise ValueError(f"No such direction: {direction} {axis}")

    def getVector(self):
        return self.vector

    def pointsTo(self, yaw: float):
        f = yaw * 0.017453292
        g = -math.sin(f)
        h = math.cos(f)
        return self.vector.getX() * g + self.vector.getZ() * h > 0.0
