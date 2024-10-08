import re
from typing import Optional, Type

MAX_FEATURE_FLAGS = 64


class FeatureUniverse:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name


class FeatureFlag:
    universe: FeatureUniverse
    mask: int

    def __init__(self, universe: FeatureUniverse, id: int) -> None:
        self.universe = universe
        self.mask = 1 << id


class FeatureSet:
    featuresMask: int
    universe: Optional[FeatureUniverse]

    def __init__(self, universe: FeatureUniverse, featuresMask: int) -> None:
        self.universe = universe
        self.featuresMask = featuresMask

    @staticmethod
    def empty():
        return FeatureSet(None, 0)

    @staticmethod
    def of(universe: FeatureUniverse, features: list[FeatureFlag]):
        if len(features) == 0:
            return FeatureSet(None, 0)
        else:
            m = FeatureSet.combineMask(universe, 0, features)
            return FeatureSet(universe, m)

    @staticmethod
    def of(feature: FeatureFlag):
        return FeatureSet(feature.universe, feature.mask)

    @staticmethod
    def of(feature1: FeatureFlag, *features: FeatureFlag):
        m = feature1 if len(features) == 0 else FeatureSet.combineMask(feature1.universe, feature1.mask, features)
        return FeatureSet(feature1.universe, m)

    @staticmethod
    def combineMask(universe: FeatureUniverse, featuresMask: int, newFeatures: list[FeatureFlag]) -> int:
        for featureFlag in newFeatures:
            if universe != featureFlag.universe:
                raise TypeError(
                    f"Mismatched feature universe, expected '{universe}', but got '{featureFlag.universe}'"
                )
            featuresMask |= featureFlag.mask

        return featuresMask

    def contains(self, feature: FeatureFlag):
        if self.universe != feature.universe:
            return False
        else:
            return (self.featuresMask & feature.mask) != 0

    def isEmpty(self):
        return self == FeatureSet.empty()

    def isSubsetOf(self, features: "FeatureSet"):
        if self.universe == None:
            return False
        elif self.universe != features.universe:
            return False
        else:
            return (self.featuresMask & ~features.featuresMask) == 0

    def intersects(self, features: "FeatureSet"):
        if self.universe is not None and features.universe is not None and self.universe == features.universe:
            return (self.featuresMask & features.featuresMask) != 0
        else:
            return False

    def __eq__(self, o: object) -> bool:
        if self == o:
            return True
        else:
            if isinstance(o, FeatureSet):
                if o.universe == self.universe and o.featuresMask == self.featuresMask:
                    return True
            return False
