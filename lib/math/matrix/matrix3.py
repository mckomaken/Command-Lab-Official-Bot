from operator import invert

from multipledispatch import dispatch

from lib.commands.util import classprop
from lib.math import Math
from lib.math.axisangle4 import AxisAngle4
from lib.math.vector.quaternion import Quaternion
from lib.math.vector.vector3 import Vector3


class Matrix3:
    m00 = classprop(float, 0)
    m01 = classprop(float, 0)
    m02 = classprop(float, 0)
    m10 = classprop(float, 0)
    m11 = classprop(float, 0)
    m12 = classprop(float, 0)
    m20 = classprop(float, 0)
    m21 = classprop(float, 0)
    m22 = classprop(float, 0)

    @dispatch()
    def __init__(self):
        self.m00 = 1.0
        self.m11 = 1.0
        self.m22 = 1.0

    @dispatch(float, float, float, float, float, float, float, float, float)
    def __init__(
        self,
        m00: float,
        m01: float,
        m02: float,
        m10: float,
        m11: float,
        m12: float,
        m20: float,
        m21: float,
        m22: float,
    ):
        self.m00 = m00
        self.m01 = m01
        self.m02 = m02
        self.m10 = m10
        self.m11 = m11
        self.m12 = m12
        self.m20 = m20
        self.m21 = m21
        self.m22 = m22

    def setTransposed(self, m: "Matrix3"):
        nm10 = m.m01()
        nm12 = m.m21()
        nm20 = m.m02()
        nm21 = m.m12()

        return self.set(m)

    @dispatch(AxisAngle4)
    def set(self, axisAngle: AxisAngle4):
        x = axisAngle.x
        y = axisAngle.y
        z = axisAngle.z
        angle = axisAngle.angle
        invLength = Math.invsqrt(x * x + y * y + z * z)
        x *= invLength
        y *= invLength
        z *= invLength
        s = Math.sin(angle)
        c = Math.cosFromSin(s, angle)
        omc = 1.0 - c
        self.m00 = c + x * x * omc
        self.m11 = c + y * y * omc
        self.m22 = c + z * z * omc
        tmp1 = x * y * omc
        tmp2 = z * s
        self.m10 = tmp1 - tmp2
        self.m01 = tmp1 + tmp2
        tmp1 = x * z * omc
        tmp2 = y * s
        self.m20 = tmp1 + tmp2
        self.m02 = tmp1 - tmp2
        tmp1 = y * z * omc
        tmp2 = x * s
        self.m21 = tmp1 - tmp2
        self.m12 = tmp1 + tmp2
        return self

    @dispatch(Quaternion)
    def set(self, q: Quaternion):
        return self.rotation(q)

    def mulSelf(self, right: "Matrix3"):
        return self.mul(right, self)

    def mul(self, right: "Matrix3", dest: "Matrix3"):
        nm00 = Math.fma(self.m00, right.m00(), Math.fma(self.m10, right.m01(), self.m20 * right.m02()))
        nm01 = Math.fma(self.m01, right.m00(), Math.fma(self.m11, right.m01(), self.m21 * right.m02()))
        nm02 = Math.fma(self.m02, right.m00(), Math.fma(self.m12, right.m01(), self.m22 * right.m02()))
        nm10 = Math.fma(self.m00, right.m10(), Math.fma(self.m10, right.m11(), self.m20 * right.m12()))
        nm11 = Math.fma(self.m01, right.m10(), Math.fma(self.m11, right.m11(), self.m21 * right.m12()))
        nm12 = Math.fma(self.m02, right.m10(), Math.fma(self.m12, right.m11(), self.m22 * right.m12()))
        nm20 = Math.fma(self.m00, right.m20(), Math.fma(self.m10, right.m21(), self.m20 * right.m22()))
        nm21 = Math.fma(self.m01, right.m20(), Math.fma(self.m11, right.m21(), self.m21 * right.m22()))
        nm22 = Math.fma(self.m02, right.m20(), Math.fma(self.m12, right.m21(), self.m22 * right.m22()))
        dest.m00 = nm00
        dest.m01 = nm01
        dest.m02 = nm02
        dest.m10 = nm10
        dest.m11 = nm11
        dest.m12 = nm12
        dest.m20 = nm20
        dest.m21 = nm21
        dest.m22 = nm22
        return dest

    def mulLocalSelf(self, left: "Matrix3"):
        return self.mulLocal(left, self)

    def mulLocal(self, left: "Matrix3", dest: "Matrix3"):
        nm00 = left.m00() * self.m00 + left.m10() * self.m01 + left.m20() * self.m02
        nm01 = left.m01() * self.m00 + left.m11() * self.m01 + left.m21() * self.m02
        nm02 = left.m02() * self.m00 + left.m12() * self.m01 + left.m22() * self.m02
        nm10 = left.m00() * self.m10 + left.m10() * self.m11 + left.m20() * self.m12
        nm11 = left.m01() * self.m10 + left.m11() * self.m11 + left.m21() * self.m12
        nm12 = left.m02() * self.m10 + left.m12() * self.m11 + left.m22() * self.m12
        nm20 = left.m00() * self.m20 + left.m10() * self.m21 + left.m20() * self.m22
        nm21 = left.m01() * self.m20 + left.m11() * self.m21 + left.m21() * self.m22
        nm22 = left.m02() * self.m20 + left.m12() * self.m21 + left.m22() * self.m22
        dest.m00 = nm00
        dest.m01 = nm01
        dest.m02 = nm02
        dest.m10 = nm10
        dest.m11 = nm11
        dest.m12 = nm12
        dest.m20 = nm20
        dest.m21 = nm21
        dest.m22 = nm22
        return dest

    @dispatch(Vector3, Vector3, Vector3)
    def set(self, col0: Vector3, col1: Vector3, col2: Vector3):
        self.m00 = col0.x()
        self.m01 = col0.y()
        self.m02 = col0.z()
        self.m10 = col1.x()
        self.m11 = col1.y()
        self.m12 = col1.z()
        self.m20 = col2.x()
        self.m21 = col2.y()
        self.m22 = col2.z()
        return self

    def determinant(self):
        return (
            (self.m00 * self.m11 - self.m01 * self.m10) * self.m22
            + (self.m02 * self.m10 - self.m00 * self.m12) * self.m21
            + (self.m01 * self.m12 - self.m02 * self.m11) * self.m20
        )

    def invertSelf(self):
        return invert(self)

    def invert(self, dest: "Matrix3"):
        a = Math.fma(self.m00, self.m11, -self.m01 * self.m10)
        b = Math.fma(self.m02, self.m10, -self.m00 * self.m12)
        c = Math.fma(self.m01, self.m12, -self.m02 * self.m11)
        d = Math.fma(a, self.m22, Math.fma(b, self.m21, c * self.m20))
        s = 1.0 / d
        nm00 = Math.fma(self.m11, self.m22, -self.m21 * self.m12) * s
        nm01 = Math.fma(self.m21, self.m02, -self.m01 * self.m22) * s
        nm02 = c * s
        nm10 = Math.fma(self.m20, self.m12, -self.m10 * self.m22) * s
        nm11 = Math.fma(self.m00, self.m22, -self.m20 * self.m02) * s
        nm12 = b * s
        nm20 = Math.fma(self.m10, self.m21, -self.m20 * self.m11) * s
        nm21 = Math.fma(self.m20, self.m01, -self.m00 * self.m21) * s
        nm22 = a * s
        dest.m00 = nm00
        dest.m01 = nm01
        dest.m02 = nm02
        dest.m10 = nm10
        dest.m11 = nm11
        dest.m12 = nm12
        dest.m20 = nm20
        dest.m21 = nm21
        dest.m22 = nm22
        return dest

    def transposeSelf(self):
        return self.transpose(self)

    def transpose(self, dest: "Matrix3"):
        return dest.set(self.m00, self.m10, self.m20, self.m01, self.m11, self.m21, self.m02, self.m12, self.m22)

    def get(self, dest):
        return dest.set(self)

    def getUnnormalizedRotation(self, dest):
        return dest.setFromUnnormalized(self)

    def getNormalizedRotation(self, dest):
        return dest.setFromNormalized(self)

    def scale(self, xyz: "Vector3", dest: "Matrix3"):
        return self.scale(xyz.x(), xyz.y(), xyz.z(), dest)

    def scaleSelf(self, xyz: "Vector3"):
        return self.scale(xyz.x(), xyz.y(), xyz.z(), self)

    def scale(self, x: float, y: float, z: float, dest: "Matrix3"):
        dest.m00 = self.m00 * x
        dest.m01 = self.m01 * x
        dest.m02 = self.m02 * x
        dest.m10 = self.m10 * y
        dest.m11 = self.m11 * y
        dest.m12 = self.m12 * y
        dest.m20 = self.m20 * z
        dest.m21 = self.m21 * z
        dest.m22 = self.m22 * z
        return dest

    def scale(self, x: float, y: float, z: float):
        return self.scale(x, y, z, self)

    def scale(self, xyz: float, dest: "Matrix3"):
        return self.scale(xyz, xyz, xyz, dest)

    def scale(self, xyz: float):
        return self.scale(xyz, xyz, xyz)

    @dispatch(float)
    def scaling(self, factor: float):
        self.m00 = factor
        self.m11 = factor
        self.m22 = factor
        return self

    @dispatch(float, float, float)
    def scaling(self, x: float, y: float, z: float):
        self.m00 = x
        self.m11 = y
        self.m22 = z
        return self

    @dispatch(float, Vector3)
    def rotation(self, angle: float, axis: Vector3):
        return self.rotation(angle, axis.x(), axis.y(), axis.z())

    @dispatch(AxisAngle4)
    def rotation(self, axisAngle: AxisAngle4):
        return self.rotation(axisAngle.angle, axisAngle.x, axisAngle.y, axisAngle.z)

    @dispatch(float, float, float, float)
    def rotation(self, angle: float, x: float, y: float, z: float):
        sin = Math.sin(angle)
        cos = Math.cosFromSin(sin, angle)
        C = 1.0 - cos
        xy = x * y
        xz = x * z
        yz = y * z
        self.m00 = cos + x * x * C
        self.m10 = xy * C - z * sin
        self.m20 = xz * C + y * sin
        self.m01 = xy * C + z * sin
        self.m11 = cos + y * y * C
        self.m21 = yz * C - x * sin
        self.m02 = xz * C - y * sin
        self.m12 = yz * C + x * sin
        self.m22 = cos + z * z * C
        return self

    def rotationX(self, ang: float):
        sin = Math.sin(ang)
        cos = Math.cosFromSin(sin, ang)
        self.m00 = 1.0
        self.m01 = 0.0
        self.m02 = 0.0
        self.m10 = 0.0
        self.m11 = cos
        self.m12 = sin
        self.m20 = 0.0
        self.m21 = -sin
        self.m22 = cos
        return self

    def rotationY(self, ang: float):
        sin = Math.sin(ang)
        cos = Math.cosFromSin(sin, ang)

        self.m00 = cos
        self.m01 = 0.0
        self.m02 = -sin
        self.m10 = 0.0
        self.m11 = 1.0
        self.m12 = 0.0
        self.m20 = sin
        self.m21 = 0.0
        self.m22 = cos
        return self

    def rotationZ(self, ang: float):
        sin = Math.sin(ang)
        cos = Math.cosFromSin(sin, ang)
        self.m00 = cos
        self.m01 = sin
        self.m02 = 0.0
        self.m10 = -sin
        self.m11 = cos
        self.m12 = 0.0
        self.m20 = 0.0
        self.m21 = 0.0
        self.m22 = 1.0
        return self

    def rotationXYZ(self, angleX: float, angleY: float, angleZ: float):
        sinX = Math.sin(angleX)
        cosX = Math.cosFromSin(sinX, angleX)
        sinY = Math.sin(angleY)
        cosY = Math.cosFromSin(sinY, angleY)
        sinZ = Math.sin(angleZ)
        cosZ = Math.cosFromSin(sinZ, angleZ)
        m_sinX = -sinX
        m_sinY = -sinY
        m_sinZ = -sinZ

        # rotateX
        nm11 = cosX
        nm12 = sinX
        nm21 = m_sinX
        nm22 = cosX
        # rotateY
        nm00 = cosY
        nm01 = nm21 * m_sinY
        nm02 = nm22 * m_sinY
        self.m20 = sinY
        self.m21 = nm21 * cosY
        self.m22 = nm22 * cosY
        # rotateZ
        self.m00 = nm00 * cosZ
        self.m01 = nm01 * cosZ + nm11 * sinZ
        self.m02 = nm02 * cosZ + nm12 * sinZ
        self.m10 = nm00 * m_sinZ
        self.m11 = nm01 * m_sinZ + nm11 * cosZ
        self.m12 = nm02 * m_sinZ + nm12 * cosZ
        return self

    @dispatch(int, int, float)
    def set(self, row: int, col: int, val: float):
        match col:
            case 0:
                match row:
                    case 0:
                        return self.m00(val)
                    case 1:
                        return self.m01(val)
                    case 2:
                        return self.m02(val)
            case 1:
                match row:
                    case 0:
                        return self.m10(val)
                    case 1:
                        return self.m11(val)
                    case 2:
                        return self.m12(val)
            case 2:
                match row:
                    case 0:
                        return self.m20(val)
                    case 1:
                        return self.m21(val)
                    case 2:
                        return self.m22(val)
        raise ValueError()
