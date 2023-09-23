import numpy as np
import math
from ursina import *
from models.reference_system import ReferenceSystem
from enum import Enum

class OrbitType(Enum):
    CIRCULAR = 1
    ELLIPTICAL = 2
    PARABOLIC = 3
    HYPERBOLIC = 4

class Orbit:
    def __init__(self, body, center_body, u):
        self.name = body.name
        self.__center_body = center_body
        position = body.get_relative_position_to(center_body)
        velocity = body.get_relative_velocity_to(center_body)
        self.__calculate_orbit(position, velocity, u)

    def get_distance_from_focal_point(self, phi):
        return self.__p / (1 + self.__e * math.cos(phi))

    def __calculate_orbit(self, position, velocity, u):
        r = np.linalg.norm(position)
        v = np.linalg.norm(velocity)
        a = 1 / (2 / r - v * v / u)
        hVector = np.array(np.cross(position, velocity))
        h = np.linalg.norm(hVector)
        p = h * h / u
        eVector = 1 / u * np.array(np.cross(velocity, hVector)) - 1 / r * np.array(position)
        e = np.linalg.norm(eVector)
        b = self.__calculate_semi_minor_axis(a, e)
        phi = self.__calculate_true_anomaly(position, r, velocity, eVector, e)
        r_min = p / (1 + e)
        i = math.acos(hVector[2] / h)
        period = 2 * math.pi * (a**3 / u)**0.5
        ae = self.__calculate_eccentric_anomaly(e, phi)
        tp = (ae-math.sin(ae))*(a**3 / u)**0.5  # perihelion passage
        p = a * (1 - e**2)

        # parameters
        self.__position = position
        self.__hVector = hVector
        self.__h = h
        self.__normalVector = hVector / h           # perpendicular vector to the plane of the orbit
        self.__shape = self.__assign_shape(e)       # orbit shape
        self.__a = a                                # semi major axis
        self.__b = b                                # semi minor axis
        self.__e = e                                # eccentricity
        self.__phi = phi                            # true anomaly
        self.__r_min = r_min                        # min distance between body and center body (focus)
        self.__period = period
        self.__tp = tp                              # perihelion passage
        self.__p = p                                # the semi-latus rectum

        # spatial points
        self.__points = self.__calculate_points()
        print(self.name, "orbit phi: ", math.degrees(self.orbit_phi), "orbit th: ", math.degrees(self.orbit_th), "fi: ", self.__phi, "first_angle: ", math.degrees(self.first_angle))

    def __calculate_eccentric_anomaly(self, e, phi, precision=1e-6, max_iter=100):
        ae = phi
        # Newtona-Raphsona method
        for _ in range(max_iter):
            f = ae - e * math.sin(ae) - phi
            df = 1 - e * math.cos(ae)
            ae -= f / df
            if abs(f) < precision:
                return ae
        return None

    def __calculate_semi_minor_axis(self, a, e):
        if e <= 1: #  ellipse case
            return a * math.sqrt(1 - e * e)
        else:      # hiperbola case
            return a * math.sqrt(e * e - 1)

    def __calculate_true_anomaly(self, position, r, velocity, eVector, e):
        dotProduct = np.dot(eVector, position) 
        if dotProduct >= 0:
            return math.acos(np.dot(eVector,position) / (e * r))    
        else:
            return 2 * math.pi - math.acos(np.dot(eVector,position) / (e * r))
    
    def __assign_shape(self, e):
        if e == 0:
            return OrbitType.CIRCULAR
        elif e > 0 and e < 1:
            return OrbitType.ELLIPTICAL
        elif e == 1:
            return OrbitType.PARABOLIC
        elif e > 1:
            return OrbitType.HYPERBOLIC
        else:
            raise Exception(f"Cannot determine the shape of the orbit for e = {e}")

    def __calculate_points(self):
        # create basic plane orbit points
        points, peri_point_index = self.__get_points_and_peri_point_index()
        # rotate basic orbit plane 
        rotation_axis = np.cross(np.array([0, 0, 1]), np.array(self.__normalVector))
        angle = math.acos(np.dot([0, 0, 1], self.__normalVector))
        self.first_angle = angle
        self.orbit_th = angle # TODO: hide it
        rotated_points = []
        for point in points:
            rotated_point = ReferenceSystem.rotate_along_axis(point, angle, rotation_axis, False)
            rotated_points.append(rotated_point)

        # find orbit direction and rotate it
        orbit_vector = rotated_points[peri_point_index]
        orbit_velocity = np.cross(orbit_vector, -self.__hVector) / self.__h**2
        orbit_velocity = orbit_velocity / np.linalg.norm(orbit_velocity)
        h_orbit = np.cross(orbit_vector, orbit_velocity)
        self.direction = orbit_velocity[1]
        print("direction: ", self.name, self.direction)
        rotation_axis = np.cross(orbit_vector, self.__position)
        angle = math.acos(np.dot(self.__normalize(orbit_vector), self.__normalize(self.__position)))
        self.orbit_phi = angle # TODO: hide it
        output_points = []
        for point in rotated_points:
            output_point = ReferenceSystem.rotate_along_axis(point, angle, np.array(rotation_axis), False)
            output_point = ReferenceSystem.rotate_along_axis(output_point, self.__phi, -np.array(rotation_axis), False)
            output_points.append(output_point)

        # move translate
        translated_points = []
        for point in output_points:
            x = point[0] + self.__center_body.position[0] / 100
            y = point[1] + self.__center_body.position[1] / 100
            z = point[2] + self.__center_body.position[2] / 100
            translated_points.append(Vec3(x, y, z))
        return translated_points

    def __get_points_and_peri_point_index(self):
        points = []
        if self.__shape == OrbitType.ELLIPTICAL:
            # create an ellipse
            for deg in range(0, 360):
                c = self.__e * self.__a 
                x = self.__a * math.sin(math.radians(deg)) - c 
                y = self.__b * math.cos(math.radians(deg))
                z = 0
                point = Vec3(x, y, z) / 100
                points.append(point)
            points.append(points[0])
            peri_point_index = 90
        else:
            # create a hiperbola
            for deg in range(-180, 180): # if change range, change peri_point_index too
                deg /= 100 
                c = self.__a - self.__r_min
                x = self.__a * math.cosh(deg) - c
                y = self.__b * math.sinh(deg)
                z = 0
                points.append(Vec3(x, y, z) / 100)
            peri_point_index = 180
        return points, peri_point_index

    def __normalize(self, vector):
        if np.linalg.norm(vector) == 0:
            return np.array([0,0,0])
        else:
            return vector / np.linalg.norm(vector)

    @property
    def shape(self):
        match self.__shape:
            case OrbitType.ELLIPTICAL:
                return "Elliptical"
            case OrbitType.HYPERBOLIC:
                return "Hyperbolic"
            case OrbitType.CIRCULAR:
                return "Circular"
            case OrbitType.PARABOLIC:
                return "Parabolic"
            case _:
                return "None"

    @property
    def semi_major_axis(self):
        return self.__a
    
    @property
    def semi_minor_axis(self):
        return self.__b

    @property
    def eccentricity(self):
        return self.__e

    @property
    def true_anomaly(self):
        return self.__phi

    @property
    def points(self):
        return self.__points

    @property
    def period(self):
        return self.__period

    @property
    def perihelion_passage(self):
        return self.__tp
    
    @property
    def semi_latus_rectum(self):
        return self.__p

    @property
    def angular_momentum(self):
        return self.__hVector

        