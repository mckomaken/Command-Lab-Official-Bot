import math

PIHalf = math.pi * 0.5
PI2 = math.pi * 2
PI = math.pi

class Math:
    @staticmethod
    def sqrt(v: float):
        return math.sqrt(v)

    @staticmethod
    def sin(v: float):
        return math.sin(v)

    @staticmethod
    def cosFromSin(sin: float, angle: float):
        cos = Math.sqrt(1.0 - sin * sin)
        a = angle + PIHalf
        b = a - int(a / PIHalf) * PI2
        if b < 0.0:
            b = PI2 + b
        if b >= PI:
            return -cos
        return cos

    @staticmethod
    def invsqrt(v: float):
        return 1.0 / Math.sqrt(v)

    @staticmethod
    def fma(a: float, b: float, c: float):
        return a * b + c