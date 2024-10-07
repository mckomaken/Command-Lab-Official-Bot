from multipledispatch import dispatch

from lib.commands.util import classprop


class Vector3:
    x = classprop(float, 0)
    y = classprop(float, 0)
    z = classprop(float, 0)

    @dispatch()
    def __init__(self):
        pass

    @dispatch(float)
    def __init__(self, d: float):
        self.x = d
        self.y = d
        self.z = d

    @dispatch(float, float, float)
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
