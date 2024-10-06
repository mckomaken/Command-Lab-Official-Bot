from lib.commands.util.math.position import Position


class Vec3d(Position):
    x: float
    y: float
    z: float

    @property
    def ZERO() -> "Vec3d":
        return Vec3d(0, 0, 0)

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def add(self, x: float, y: float, z: float):
        return Vec3d(self.x + x, self.y + y, self.z + z)
