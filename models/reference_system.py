import math
import numpy as np
from mathematica.vector import Vector
class ReferenceSystem:
    def __init__(self, origin, point):
        self.x = point[0] - origin[0]
        self.y = point[1] - origin[1]
        self.z = point[2] - origin[2]
        self.r = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        self.phi = self.__calculate_phi()
        self.th = self.__calculate_th()

    @staticmethod
    def rotate_along_axis(point, angle, rot_axis, degrees = False):
        if not np.any(rot_axis):
            return point
        if degrees:
            angle = angle * math.pi / 180
        norm_rot_axis = rot_axis.normalize()
        point_quaternion = np.quaternion(0, point[0], point[1], point[2])
        sin = math.sin(angle / 2)
        q = np.quaternion(math.cos(angle / 2), sin * norm_rot_axis.x, sin * norm_rot_axis.y, sin * norm_rot_axis.z)
        conjugate_q = np.conjugate(q)
        result_point_quaternion = q * point_quaternion * conjugate_q
        return np.array([result_point_quaternion.x, result_point_quaternion.y, result_point_quaternion.z])
    
    def __calculate_phi(self):
        x = self.x
        y = self.y
        z = self.z
        if x > 0 and y >= 0:
            return math.atan(y / x)
        elif x < 0:
            return math.atan(y / x) + math.pi
        elif x > 0 and y < 0:
            return math.atan(y / x) + 2 * math.pi
        elif x == 0 and y > 0:
            return math.pi / 2
        elif x == 0 and y < 0:
            return 3 * math.pi / 2
        else:
            return 0.0

    def __calculate_th(self):
        r = math.sqrt(self.x**2 + self.z**2) * 1.0
        if r == 0:
            return 0.0
        result = math.asin(self.z / r)
        if math.isnan(result):
            return 0.0
        else:
            return result
