import math
import ursina as urs

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def normalize(self):
        r = self.magnitude()
        if r == 0:
            return Vector.zeros()
        self.x /= r 
        self.y /= r 
        self.z /= r 
        return self

    def get_normalize(self):
        r = self.magnitude()
        if r == 0:
            return Vector.zeros()
        x = self.x / r 
        y = self.y / r 
        z = self.z / r 
        return Vector(x, y, z)
    
    def cross(self, vector):
        return Vector(self.y * vector.z - self.z * vector.y, self.z * vector.x - self.x * vector.z, self.x * vector.y - self.y * vector.x)

    def to_urs_Vec3(self):
        return urs.Vec3(self.x, self.y, self.z)

    def round8(self):
        self.x = round(self.x, 8)
        self.y = round(self.y, 8)
        self.z = round(self.z, 8)
        return self

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z )

    def __rmul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z )

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    @staticmethod
    def zeros():
        return Vector(0, 0, 0)

    @staticmethod
    def ones():
        return Vector(1, 1, 1)

    @staticmethod
    def X():
        return Vector(1, 0, 0)

    @staticmethod
    def Y():
        return Vector(0, 1, 0)

    @staticmethod
    def Z():
        return Vector(0, 0, 1)

if __name__ == '__main__':
    x = Vector(100, 0, 50)
    y = Vector(0, 1, 0)
    print(x / 50)