from enum import Enum

from lib.commands.util.axis_transformation import AxisTransformation
from lib.commands.util.direction import Axis, Direction
from lib.commands.util.pair import Pair
from lib.math.matrix.matrix3 import Matrix3


class DirectionTransformation(Enum):
    IDENTITY = ("identity", AxisTransformation.P123, False, False, False)
    ROT_180_FACE_XY = ("rot_180_face_xy", AxisTransformation.P123, True, True, False)
    ROT_180_FACE_XZ = ("rot_180_face_xz", AxisTransformation.P123, True, False, True)
    ROT_180_FACE_YZ = ("rot_180_face_yz", AxisTransformation.P123, False, True, True)
    ROT_120_NNN = ("rot_120_nnn", AxisTransformation.P231, False, False, False)
    ROT_120_NNP = ("rot_120_nnp", AxisTransformation.P312, True, False, True)
    ROT_120_NPN = ("rot_120_npn", AxisTransformation.P312, False, True, True)
    ROT_120_NPP = ("rot_120_npp", AxisTransformation.P231, True, False, True)
    ROT_120_PNN = ("rot_120_pnn", AxisTransformation.P312, True, True, False)
    ROT_120_PNP = ("rot_120_pnp", AxisTransformation.P231, True, True, False)
    ROT_120_PPN = ("rot_120_ppn", AxisTransformation.P231, False, True, True)
    ROT_120_PPP = ("rot_120_ppp", AxisTransformation.P312, False, False, False)
    ROT_180_EDGE_XY_NEG = ("rot_180_edge_xy_neg", AxisTransformation.P213, True, True, True)
    ROT_180_EDGE_XY_POS = ("rot_180_edge_xy_pos", AxisTransformation.P213, False, False, True)
    ROT_180_EDGE_XZ_NEG = ("rot_180_edge_xz_neg", AxisTransformation.P321, True, True, True)
    ROT_180_EDGE_XZ_POS = ("rot_180_edge_xz_pos", AxisTransformation.P321, False, True, False)
    ROT_180_EDGE_YZ_NEG = ("rot_180_edge_yz_neg", AxisTransformation.P132, True, True, True)
    ROT_180_EDGE_YZ_POS = ("rot_180_edge_yz_pos", AxisTransformation.P132, True, False, False)
    ROT_90_X_NEG = ("rot_90_x_neg", AxisTransformation.P132, False, False, True)
    ROT_90_X_POS = ("rot_90_x_pos", AxisTransformation.P132, False, True, False)
    ROT_90_Y_NEG = ("rot_90_y_neg", AxisTransformation.P321, True, False, False)
    ROT_90_Y_POS = ("rot_90_y_pos", AxisTransformation.P321, False, False, True)
    ROT_90_Z_NEG = ("rot_90_z_neg", AxisTransformation.P213, False, True, False)
    ROT_90_Z_POS = ("rot_90_z_pos", AxisTransformation.P213, True, False, False)
    INVERSION = ("inversion", AxisTransformation.P123, True, True, True)
    INVERT_X = ("invert_x", AxisTransformation.P123, True, False, False)
    INVERT_Y = ("invert_y", AxisTransformation.P123, False, True, False)
    INVERT_Z = ("invert_z", AxisTransformation.P123, False, False, True)
    ROT_60_REF_NNN = ("rot_60_ref_nnn", AxisTransformation.P312, True, True, True)
    ROT_60_REF_NNP = ("rot_60_ref_nnp", AxisTransformation.P231, True, False, False)
    ROT_60_REF_NPN = ("rot_60_ref_npn", AxisTransformation.P231, False, False, True)
    ROT_60_REF_NPP = ("rot_60_ref_npp", AxisTransformation.P312, False, False, True)
    ROT_60_REF_PNN = ("rot_60_ref_pnn", AxisTransformation.P231, False, True, False)
    ROT_60_REF_PNP = ("rot_60_ref_pnp", AxisTransformation.P312, True, False, False)
    ROT_60_REF_PPN = ("rot_60_ref_ppn", AxisTransformation.P312, False, True, False)
    ROT_60_REF_PPP = ("rot_60_ref_ppp", AxisTransformation.P231, True, True, True)
    SWAP_XY = ("swap_xy", AxisTransformation.P213, False, False, False)
    SWAP_YZ = ("swap_yz", AxisTransformation.P132, False, False, False)
    SWAP_XZ = ("swap_xz", AxisTransformation.P321, False, False, False)
    SWAP_NEG_XY = ("swap_neg_xy", AxisTransformation.P213, True, True, False)
    SWAP_NEG_YZ = ("swap_neg_yz", AxisTransformation.P132, False, True, True)
    SWAP_NEG_XZ = ("swap_neg_xz", AxisTransformation.P321, True, False, True)
    ROT_90_REF_X_NEG = ("rot_90_ref_x_neg", AxisTransformation.P132, True, False, True)
    ROT_90_REF_X_POS = ("rot_90_ref_x_pos", AxisTransformation.P132, True, True, False)
    ROT_90_REF_Y_NEG = ("rot_90_ref_y_neg", AxisTransformation.P321, True, True, False)
    ROT_90_REF_Y_POS = ("rot_90_ref_y_pos", AxisTransformation.P321, False, True, True)
    ROT_90_REF_Z_NEG = ("rot_90_ref_z_neg", AxisTransformation.P213, False, True, True)
    ROT_90_REF_Z_POS = ("rot_90_ref_z_pos", AxisTransformation.P213, True, False, True)

    @staticmethod
    def values():
        return [v for v in DirectionTransformation]

    def ordinal():
        return

    @staticmethod
    @property
    def COMBINATIONS():
        directionTransformations: list[list[DirectionTransformation]]
        mapping = dict()
        for directionTransformationx in DirectionTransformation.values():
            mapping[Pair.of(directionTransformationx.axisTransformation, directionTransformationx.getAxisFlips())] = (
                directionTransformationx
            )

        for directionTransformation in DirectionTransformation.values():
            for directionTransformation2 in DirectionTransformation.values():
                booleanList = directionTransformation.getAxisFlips()
                booleanList2 = directionTransformation2.getAxisFlips()
                axisTransformation = directionTransformation2.axisTransformation.prepend(
                    directionTransformation.axisTransformation
                )
                booleanArrayList = list()

                for i in range(3):
                    booleanArrayList.append(
                        booleanList[i] ^ booleanList2[directionTransformation.axisTransformation.map(i)]
                    )
                directionTransformations[directionTransformation.ordinal()][directionTransformation2.ordinal()] = (
                    mapping.get(Pair.of(axisTransformation, booleanArrayList))
                )

    @staticmethod
    @property
    def INVERSES():
        def _map(directionTransformation: DirectionTransformation):
            return [d for d in directionTransformation.values() if d.prepend(d) == DirectionTransformation.IDENTITY]

        return map(_map, DirectionTransformation.values())

    def __init__(self, name: str, axisTransformation: AxisTransformation, flipX: bool, flipY: bool, flipZ: bool):
        self._name = name
        self.flipX = flipX
        self.flipY = flipY
        self.flipZ = flipZ
        self.axisTransformation = axisTransformation
        self.matrix = Matrix3().scaling(-1.0 if flipX else 1.0, -1.0 if flipY else 1.0, -1.0 if flipZ else 1.0)
        self.matrix.mulSelf(axisTransformation.getMatrix())

    def getAxisFlips(self):
        return [self.flipX, self.flipY, self.flipZ]

    def prepend(self, transformation: "DirectionTransformation"):
        return self.COMBINATIONS[self.ordinal()][transformation.ordinal()]

    def inverse(self) -> "DirectionTransformation":
        return self.INVERSES[self.ordinal()]

    def getMatrix(self):
        return Matrix3(self.matrix)

    def __str__(self):
        return self.name

    def map(self, direction: "Direction"):
        if self.mappings == None:
            self.mappings: dict[Direction, Direction] = dict()
            axiss = Axis.values()

            for direction2 in Direction:
                axis = direction2.getAxis()
                axisDirection = direction2.getDirection()
                axis2 = axiss[self.axisTransformation.map(axis.ordinal())]
                axisDirection2 = axisDirection.getOpposite() if self.shouldFlipDirection(axis2) else axisDirection
                direction3 = Direction.fromAxis(axis2, axisDirection2)
                self.mappings[direction2] = direction3

        return self.mappings.get(direction)

    def shouldFlipDirection(self, axis: "Axis"):
        match axis:
            case Axis.X:
                return self.flipX
            case Axis.Y:
                return self.flipY
            case Axis.Z, _:
                return self.flipZ
