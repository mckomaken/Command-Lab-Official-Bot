from enum import Enum


from lib.commands.util import Util
from lib.math.matrix.matrix3 import Matrix3


class AxisTransformation(Enum):
    P123 = (0, 1, 2)
    P213 = (1, 0, 2)
    P132 = (0, 2, 1)
    P231 = (1, 2, 0)
    P312 = (2, 0, 1)
    P321 = (2, 1, 0)

    @staticmethod
    @property
    def COMBINATIONS():
        def _map(axisTransformations: AxisTransformation):
            for axisTransformation in AxisTransformation:
                for axisTransformation2 in AxisTransformation:
                    _is = list()

                    for i in range(3):
                        _is[i] = axisTransformation.mappings[axisTransformation2.mappings[i]]

                    axisTransformation3 = [x for x in AxisTransformation if x.mappings == _is][0]

                    axisTransformations[axisTransformation.ordinal()][
                        axisTransformation2.ordinal()
                    ] = axisTransformation3

        return Util.make(AxisTransformation, _map)

    def __init__(self, xMapping: int, yMapping: int, zMapping: int):
        self.mappings = [xMapping, yMapping, zMapping]
        self.matrix = Matrix3()
        self.matrix.set(self.map(0), 0, 1.0)
        self.matrix.set(self.map(1), 1, 1.0)
        self.matrix.set(self.map(2), 2, 1.0)

    def ordinal(self):
        return list(AxisTransformation).index(self)

    def prepend(self, transformation: "AxisTransformation"):
        return AxisTransformation.COMBINATIONS[self.ordinal()][transformation.ordinal()]

    def map(self, oldAxis: int):
        return self.mappings[oldAxis]

    def getMatrix(self):
        return self.matrix
