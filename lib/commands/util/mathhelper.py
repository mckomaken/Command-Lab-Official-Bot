import math


class MathHelper:
    @staticmethod
    def wrapDegrees(degrees: float) -> float:
        f = degrees % 360.0
        if f >= 180.0:
            f -= 360.0

        if f < -180.0:
            f += 360.0

        return f

    @staticmethod
    def lerp(delta: float, start: float, end: float):
        return start + delta * (end - start)

    @staticmethod
    def squaredMagnitude(a: float, b: float, c: float):
        return a * a + b * b + c * c

    @staticmethod
    def floor(a: float):
        return math.floor(a)
