from lib.commands.util import classprop


class AxisAngle4:
    angle = classprop(float, 0)
    x = classprop(float, 0)
    y = classprop(float, 0)
    z = classprop(float, 0)

    def __init__(self) -> None:
        self.z = 1