from math import isnan
from multipledispatch import dispatch
from typing import Optional
from lib.commands.util.hit_result import BlockHitResult
from lib.commands.util.math.block_box import BlockBox
from lib.commands.util.math.vec3d import Vec3d
from lib.commands.util.direction import Axis, Direction
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.util.mathhelper import MathHelper


def _compare(x: float, y: float):
    if x < y:
        return -1
    if x > y:
        return 1
    if x == y:
        return 0


class Box:
    EPSILON = 1.0e-7
    minX: float
    minY: float
    minZ: float
    maxX: float
    maxY: float
    maxZ: float

    def __init__(self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
        self.minX = min(x1, x2)
        self.minY = min(y1, y2)
        self.minZ = min(z1, z2)
        self.maxX = max(x1, x2)
        self.maxY = max(y1, y2)
        self.maxZ = max(z1, z2)

    @staticmethod
    def fromBlockPos(pos: BlockPos):
        return Box(pos.getX(), pos.getY(), pos.getZ(), (pos.getX() + 1), (pos.getY() + 1), (pos.getZ() + 1))

    @staticmethod
    def fromVec3d2(pos1: Vec3d, pos2: Vec3d):
        return Box(pos1.x, pos1.y, pos1.z, pos2.x, pos2.y, pos2.z)

    @staticmethod
    def fromBlockBox(mutable: "BlockBox"):
        return Box(
            mutable.getMinX(),
            mutable.getMinY(),
            mutable.getMinZ(),
            (mutable.getMaxX() + 1),
            (mutable.getMaxY() + 1),
            (mutable.getMaxZ() + 1),
        )

    @staticmethod
    def fromVec3d(pos: Vec3d):
        return Box(pos.x, pos.y, pos.z, pos.x + 1.0, pos.y + 1.0, pos.z + 1.0)

    @staticmethod
    def enclosing(pos1: BlockPos, pos2: BlockPos):
        return Box(
            min(pos1.getX(), pos2.getX()),
            min(pos1.getY(), pos2.getY()),
            min(pos1.getZ(), pos2.getZ()),
            (max(pos1.getX(), pos2.getX()) + 1),
            (max(pos1.getY(), pos2.getY()) + 1),
            (max(pos1.getZ(), pos2.getZ()) + 1),
        )

    def withMinX(self, minX: float):
        return Box(minX, self.minY, self.minZ, self.maxX, self.maxY, self.maxZ)

    def withMinY(self, minY: float):
        return Box(self.minX, minY, self.minZ, self.maxX, self.maxY, self.maxZ)

    def withMinZ(self, minZ: float):
        return Box(self.minX, self.minY, minZ, self.maxX, self.maxY, self.maxZ)

    def withMaxX(self, maxX: float):
        return Box(self.minX, self.minY, self.minZ, maxX, self.maxY, self.maxZ)

    def withMaxY(self, maxY: float):
        return Box(self.minX, self.minY, self.minZ, self.maxX, maxY, self.maxZ)

    def withMaxZ(self, maxZ: float):
        return Box(self.minX, self.minY, self.minZ, self.maxX, self.maxY, maxZ)

    def getMin(self, axis: Axis):
        return axis.choose(self.minX, self.minY, self.minZ)

    def getMax(self, axis: Axis):
        return axis.choose(self.maxX, self.maxY, self.maxZ)

    def __eq__(self, o: object) -> bool:
        if self == o:
            return True
        elif not isinstance(o, Box):
            return False
        else:
            if _compare(o.minX, self.minX) != 0:
                return False
            elif _compare(o.minY, self.minY) != 0:
                return False
            elif _compare(o.minZ, self.minZ) != 0:
                return False
            elif _compare(o.maxX, self.maxX) != 0:
                return False
            elif _compare(o.maxY, self.maxY) != 0:
                return False
            else:
                return _compare(o.maxZ, self.maxZ) == 0

    def shrink(self, x: float, y: float, z: float):
        d = self.minX
        e = self.minY
        f = self.minZ
        g = self.maxX
        h = self.maxY
        i = self.maxZ
        if x < 0.0:
            d -= x
        elif x > 0.0:
            g -= x

        if y < 0.0:
            e -= y
        elif y > 0.0:
            h -= y

        if z < 0.0:
            f -= z
        elif z > 0.0:
            i -= z

        return Box(d, e, f, g, h, i)

    @dispatch(Vec3d)
    def stretch(self, scale: Vec3d):
        return self.stretch(scale.x, scale.y, scale.z)

    @dispatch(float, float, float)
    def stretch(self, x: float, y: float, z: float):
        d = self.minX
        e = self.minY
        f = self.minZ
        g = self.maxX
        h = self.maxY
        i = self.maxZ
        if x < 0.0:
            d += x
        elif x > 0.0:
            g += x

        if y < 0.0:
            e += y
        elif y > 0.0:
            h += y

        if z < 0.0:
            f += z
        elif z > 0.0:
            i += z

        return Box(d, e, f, g, h, i)

    @dispatch(float, float, float)
    def expand(self, x: float, y: float, z: float):
        d = self.minX - x
        e = self.minY - y
        f = self.minZ - z
        g = self.maxX + x
        h = self.maxY + y
        i = self.maxZ + z
        return Box(d, e, f, g, h, i)

    @dispatch(Vec3d)
    def expand(self, value: Vec3d):
        return self.expand(value, value, value)

    def intersection(self, box: "Box"):
        d = max(self.minX, box.minX)
        e = max(self.minY, box.minY)
        f = max(self.minZ, box.minZ)
        g = min(self.maxX, box.maxX)
        h = min(self.maxY, box.maxY)
        i = min(self.maxZ, box.maxZ)
        return Box(d, e, f, g, h, i)

    def union(self, box: "Box"):
        d = min(self.minX, box.minX)
        e = min(self.minY, box.minY)
        f = min(self.minZ, box.minZ)
        g = max(self.maxX, box.maxX)
        h = max(self.maxY, box.maxY)
        i = max(self.maxZ, box.maxZ)
        return Box(d, e, f, g, h, i)

    @dispatch(float, float, float)
    def offset(self, x: float, y: float, z: float):
        return Box(self.minX + x, self.minY + y, self.minZ + z, self.maxX + x, self.maxY + y, self.maxZ + z)

    @dispatch(BlockPos)
    def offset(self, blockPos: BlockPos):
        return Box(
            self.minX + blockPos.getX(),
            self.minY + blockPos.getY(),
            self.minZ + blockPos.getZ(),
            self.maxX + blockPos.getX(),
            self.maxY + blockPos.getY(),
            self.maxZ + blockPos.getZ(),
        )

    @dispatch(Vec3d)
    def offset(self, vec: Vec3d):
        return self.offset(vec.x, vec.y, vec.z)

    def intersects(self, box: "Box"):
        return self.intersects(box.minX, box.minY, box.minZ, box.maxX, box.maxY, box.maxZ)

    def intersects(self, minX, minY, minZ, maxX, maxY, maxZ):
        return (
            self.minX < maxX
            and self.maxX > minX
            and self.minY < maxY
            and self.maxY > minY
            and self.minZ < maxZ
            and self.maxZ > minZ
        )

    def intersects(self, pos1: Vec3d, pos2: Vec3d):
        return self.intersects(
            min(pos1.x, pos2.x),
            min(pos1.y, pos2.y),
            min(pos1.z, pos2.z),
            max(pos1.x, pos2.x),
            max(pos1.y, pos2.y),
            max(pos1.z, pos2.z),
        )

    @dispatch(Vec3d)
    def contains(self, pos: Vec3d):
        return self.contains(pos.x, pos.y, pos.z)

    @dispatch(float, float, float)
    def contains(self, x, y, z):
        return (
            x >= self.minX and x < self.maxX and y >= self.minY and y < self.maxY and z >= self.minZ and z < self.maxZ
        )

    def getAverageSideLength(self):
        d = self.getLengthX()
        e = self.getLengthY()
        f = self.getLengthZ()
        return (d + e + f) / 3.0

    def getLengthX(self):
        return self.maxX - self.minX

    def getLengthY(self):
        return self.maxY - self.minY

    def getLengthZ(self):
        return self.maxZ - self.minZ

    @dispatch(float, float, float)
    def contract(self, x, y, z):
        return self.expand(-x, -y, -z)

    @dispatch(Vec3d)
    def contract(self, value: Vec3d):
        return self.expand(-value)

    @dispatch(Vec3d, Vec3d)
    def raycast(self, min: Vec3d, max: Vec3d) -> Optional[Vec3d]:
        ds = [1.0]
        d = max.x - min.x
        e = max.y - min.y
        f = max.z - min.z
        direction = self.traceCollisionSide(self, min, ds, None, d, e, f)
        if direction is None:
            return None
        else:
            g = ds[0]
            return min.add(g * d, g * e, g * f)

    @dispatch(list["Box"], Vec3d, Vec3d, BlockPos)
    def raycast(self, boxes: list["Box"], fro: Vec3d, to: Vec3d, pos: BlockPos):
        ds = [1.0]
        direction = None
        d = to.x - fro.x
        e = to.y - fro.y
        f = to.z - fro.z

        for box in boxes:
            direction = self.traceCollisionSide(box.offset(pos), fro, ds, direction, d, e, f)

        if direction is None:
            return None
        else:
            g = ds[0]
            return BlockHitResult(fro.add(g * d, g * e, g * f), direction, pos, False)

    @staticmethod
    def traceCollisionSide(
        box: "Box",
        intersectingVector: Vec3d,
        traceDistanceResult: list[float],
        approachDirection: Direction,
        deltaX,
        deltaY,
        deltaZ,
    ):
        if deltaX > 1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaX,
                deltaY,
                deltaZ,
                box.minX,
                box.minY,
                box.maxY,
                box.minZ,
                box.maxZ,
                Direction.WEST,
                intersectingVector.x,
                intersectingVector.y,
                intersectingVector.z,
            )
        elif deltaX < -1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaX,
                deltaY,
                deltaZ,
                box.maxX,
                box.minY,
                box.maxY,
                box.minZ,
                box.maxZ,
                Direction.EAST,
                intersectingVector.x,
                intersectingVector.y,
                intersectingVector.z,
            )

        if deltaY > 1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaY,
                deltaZ,
                deltaX,
                box.minY,
                box.minZ,
                box.maxZ,
                box.minX,
                box.maxX,
                Direction.DOWN,
                intersectingVector.y,
                intersectingVector.z,
                intersectingVector.x,
            )
        elif deltaY < -1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaY,
                deltaZ,
                deltaX,
                box.maxY,
                box.minZ,
                box.maxZ,
                box.minX,
                box.maxX,
                Direction.UP,
                intersectingVector.y,
                intersectingVector.z,
                intersectingVector.x,
            )

        if deltaZ > 1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaZ,
                deltaX,
                deltaY,
                box.minZ,
                box.minX,
                box.maxX,
                box.minY,
                box.maxY,
                Direction.NORTH,
                intersectingVector.z,
                intersectingVector.x,
                intersectingVector.y,
            )
        elif deltaZ < -1.0e-7:
            approachDirection = Box.traceCollisionSide(
                traceDistanceResult,
                approachDirection,
                deltaZ,
                deltaX,
                deltaY,
                box.maxZ,
                box.minX,
                box.maxX,
                box.minY,
                box.maxY,
                Direction.SOUTH,
                intersectingVector.z,
                intersectingVector.x,
                intersectingVector.y,
            )

        return approachDirection

    @staticmethod
    def traceCollisionSide(
        traceDistanceResult: list[float],
        approachDirection: Direction,
        deltaX,
        deltaY,
        deltaZ,
        begin,
        minX,
        maxX,
        minZ,
        maxZ,
        resultDirection: Direction,
        startX,
        startY,
        startZ,
    ):
        d = (begin - startX) / deltaX
        e = startY + d * deltaY
        f = startZ + d * deltaZ
        if (
            0.0 < d
            and d < traceDistanceResult[0]
            and minX - 1.0e-7 < e
            and e < maxX + 1.0e-7
            and minZ - 1.0e-7 < f
            and f < maxZ + 1.0e-7
        ):
            traceDistanceResult[0] = d
            return resultDirection
        else:
            return approachDirection

    def squaredMagnitude(self, pos: Vec3d):
        d = max(max(self.minX - pos.x, pos.x - self.maxX), 0.0)
        e = max(max(self.minY - pos.y, pos.y - self.maxY), 0.0)
        f = max(max(self.minZ - pos.z, pos.z - self.maxZ), 0.0)
        return MathHelper.squaredMagnitude(d, e, f)

    def __str__(self) -> str:
        return (
            "AABB["
            + self.minX
            + ", "
            + self.minY
            + ", "
            + self.minZ
            + "] -> ["
            + self.maxX
            + ", "
            + self.maxY
            + ", "
            + self.maxZ
            + "]"
        )

    def isNaN(self):
        return (
            isnan(self.minX)
            or isnan(self.minY)
            or isnan(self.minZ)
            or isnan(self.maxX)
            or isnan(self.maxY)
            or isnan(self.maxZ)
        )

    def getCenter(self):
        return Vec3d(
            MathHelper.lerp(0.5, self.minX, self.maxX),
            MathHelper.lerp(0.5, self.minY, self.maxY),
            MathHelper.lerp(0.5, self.minZ, self.maxZ),
        )

    def getBottomCenter(self):
        return Vec3d(MathHelper.lerp(0.5, self.minX, self.maxX), self.minY, MathHelper.lerp(0.5, self.minZ, self.maxZ))

    def getMinPos(self):
        return Vec3d(self.minX, self.minY, self.minZ)

    def getMaxPos(self):
        return Vec3d(self.maxX, self.maxY, self.maxZ)

    @staticmethod
    def of(center: Vec3d, dx, dy, dz) -> "Box":
        return Box(
            center.x - dx / 2.0,
            center.y - dy / 2.0,
            center.z - dz / 2.0,
            center.x + dx / 2.0,
            center.y + dy / 2.0,
            center.z + dz / 2.0,
        )
