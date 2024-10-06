from lib.commands.util.math.position import Position


class Vec3i(Position):
    x: int
    y: int
    z: int

    @property
    def ZERO() -> "Vec3i":
        return Vec3i(0, 0, 0)

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def add(self, x: int, y: int, z: int):
        return Vec3i(self.x + x, self.y + y, self.z + z)
