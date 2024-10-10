from enum import Enum

from lib.commands import util
from lib.commands.util.direction import Axis, Direction
from lib.commands.util.direction_transformation import DirectionTransformation
from lib.commands.util.random import Random


class BlockRotation(Enum):
    NONE = (0, "none", DirectionTransformation.IDENTITY)
    CLOCKWISE_90 = (1, "clockwise_90", DirectionTransformation.ROT_90_Y_NEG)
    CLOCKWISE_180 = (2, "180", DirectionTransformation.ROT_180_FACE_XZ)
    COUNTERCLOCKWISE_90 = (
        3,
        "counterclockwise_90",
        DirectionTransformation.ROT_90_Y_POS,
    )

    @staticmethod
    def values():
        return [v for v in BlockRotation]

    def ordinal(self):
        return self._ordinal

    def __init__(
        self, ordinal: int, id: str, directionTransformation: DirectionTransformation
    ):
        self._ordinal = ordinal
        self.id = id
        self.directionTransformation = directionTransformation

    def rotate(self, rotation: "BlockRotation") -> "BlockRotation":
        match rotation.ordinal():
            case 2:
                match self.ordinal():
                    case 0:
                        return BlockRotation.CLOCKWISE_180
                    case 1:
                        return BlockRotation.COUNTERCLOCKWISE_90
                    case 2:
                        return BlockRotation.NONE
                    case 3:
                        return BlockRotation.CLOCKWISE_90

            case 3:
                match self.ordinal():
                    case 0:
                        return BlockRotation.COUNTERCLOCKWISE_90
                    case 1:
                        return BlockRotation.NONE
                    case 2:
                        return BlockRotation.CLOCKWISE_90
                    case 3:
                        return BlockRotation.CLOCKWISE_180

            case 1:
                match self.ordinal():
                    case 0:
                        return BlockRotation.CLOCKWISE_90
                    case 1:
                        return BlockRotation.CLOCKWISE_180
                    case 2:
                        return BlockRotation.COUNTERCLOCKWISE_90
                    case 3:
                        return BlockRotation.NONE

            case _:
                return self

    def getDirectionTransformation(self):
        return self.directionTransformation

    def rotateDirection(self, direction: Direction):
        if direction.getAxis() == Axis.Y:
            return direction
        else:
            match self.ordinal():
                case 1:
                    return direction.rotateYClockwise()
                case 2:
                    return direction.getOpposite()
                case 3:
                    return direction.rotateYCounterclockwise()
                case _:
                    return direction

    def rotateCount(self, rotation: int, fullTurn: int):
        match self.ordinal():
            case 1:
                return (rotation + fullTurn / 4) % fullTurn
            case 2:
                return (rotation + fullTurn / 2) % fullTurn
            case 3:
                return (rotation + fullTurn * 3 / 4) % fullTurn
            case _:
                return rotation

    @staticmethod
    def random(random: Random):
        return util.getRandom(BlockRotation.values(), random)

    def randomRotationOrder(random: Random):
        return util.copyShuffled(BlockRotation.values(), random)

    def asString(self):
        return self.id
