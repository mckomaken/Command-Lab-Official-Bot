import re
from enum import Enum

from multipledispatch import dispatch

from lib.commands.util.direction import Direction
from lib.commands.util.math.block_pos import BlockPos
from lib.commands.util.math.vec3d import Vec3d


class HitType(Enum):
    MISS = 0
    BLOCK = 1
    ENTITY = 2


class HitResult:
    def __init__(self, pos: Vec3d) -> None:
        self.pos = pos

    def getType(self) -> HitType:
        raise NotImplementedError()

    def getPos(self):
        return self.pos


class BlockHitResult(HitResult):
    @dispatch(Vec3d, Direction, BlockPos, bool)
    def __init__(self, pos: Vec3d, side: Direction, blockPos: BlockPos, insideBlock: bool) -> None:
        self.__init__(False, pos, side, blockPos, insideBlock)

    @dispatch(bool, Vec3d, Direction, BlockPos, bool)
    def __init__(self, missed: bool, pos: Vec3d, side: Direction, blockPos: BlockPos, insideBlock: bool):
        super(pos)
        self.missed = missed
        self.side = side
        self.blockPos = blockPos
        self.insideBlock = insideBlock

    def withSide(self, side: Direction):
        return BlockHitResult(self.missed, self.pos, side, self.blockPos, self.insideBlock)

    def withBlockPos(self, blockPos: BlockPos):
        return BlockHitResult(self.missed, self.pos, self.side, blockPos, self.insideBlock)

    @staticmethod
    def createMissed(pos: Vec3d, side: Direction, blockPos: BlockPos):
        return BlockHitResult(True, pos, side, blockPos, False)

    def getType(self) -> HitType:
        return HitType.MISS if self.missed else HitType.BLOCK
