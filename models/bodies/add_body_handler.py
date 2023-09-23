from models.bodies.body_type import BodyType
from models.bodies.sphere_body import SphereBody
from models.bodies.shuttle_body import ShuttleBody
from mathematica.vector import Vector
import numpy as np

class AddBodyHandler():
    @staticmethod
    def add_planets(body_system):
        AddBodyHandler.__add_sun(body_system)
        AddBodyHandler.__add_test1(body_system)
        AddBodyHandler.__add_test2(body_system)
        AddBodyHandler.__add_test3(body_system)
        # AddBodyHandler.__add_test4(body_system)
        AddBodyHandler.__add_test5(body_system)
        AddBodyHandler.__add_test6(body_system)
        # AddBodyHandler.__add_mercury(body_system)
        # AddBodyHandler.__add_venus(body_system)
        # AddBodyHandler.__add_earth(body_system) 
        # AddBodyHandler.__add_moon(body_system) 
        # AddBodyHandler.__add_mars(body_system)
        # self.__add_jupiter()
        # self.__add_neptune()

    @staticmethod
    def add_shuttle(body_system):
        AddBodyHandler.__add_shuttle(body_system)

    @staticmethod
    def __add_test1(body_system):
        body = SphereBody(name = "test1", position = 50 * Vector.X(), velocity = 17 * Vector.Y(), mass = 10, radius = 0.5)
        body_system.add_body(body)
    
    @staticmethod
    def __add_test2(body_system):
        body = SphereBody(name = "test2", position = -50 * Vector.X(), velocity = 17 * Vector.Y(), mass = 10, radius = 0.5)
        body_system.add_body(body)
    
    @staticmethod
    def __add_test3(body_system):
        body = SphereBody(name = "test3", position = 50 * Vector.X(), velocity = 17 * Vector.Z(), mass = 10, radius = 0.5)
        body_system.add_body(body)
    
    @staticmethod
    def __add_test4(body_system):
        body = SphereBody(name = "test4", position = 50 * Vector.X(), velocity = -17 * Vector.Y(), mass = 10, radius = 0.5)
        body_system.add_body(body)
    
    @staticmethod
    def __add_test5(body_system):
        body = SphereBody(name = "test5", position = -50 * Vector.Z(), velocity = 17 * Vector.Y(), mass = 10, radius = 0.5)
        body_system.add_body(body)
    
    @staticmethod
    def __add_test6(body_system):
        body = SphereBody(name = "test6", position = 50 * Vector.Z(), velocity = 17 * Vector.Y(), mass = 10, radius = 0.5)
        body_system.add_body(body)

    @staticmethod
    def __add_sun(body_system):
        body = SphereBody(name = "Sun", position = Vector.zeros(), velocity = Vector.zeros(), mass = 10000, radius = 2)
        body_system.add_body(body)
    
    @staticmethod
    def __add_mercury(body_system):
        mercury = SphereBody(name = "Mercury", position = np.array([35.0, 15, 10]), velocity = np.array([15, 5, 12]), mass = 10, radius = 0.5)
        body_system.add_body(mercury)

    @staticmethod
    def __add_venus(body_system):
        venus = SphereBody(name = "Venus", position = np.array([-75.0, -75, 0]), velocity = np.array([0, 5, 0]), mass = 1, radius = 1)
        body_system.add_body(venus)

    @staticmethod
    def __add_earth(body_system):
        body = SphereBody(name = "Earth", position = np.array([100.0, 0, 0]), velocity = np.array([0, 17, 0]), mass = 100, radius = 1)
        body_system.add_body(body)

    @staticmethod
    def __add_moon(body_system):
        body = SphereBody(name = "Moon", position = np.array([100.0, 10, 0]), velocity = np.array([0, 17, 3]), mass = 1, radius = 0.2)
        body_system.add_body(body)
    
    @staticmethod
    def __add_mars(body_system):
        body = SphereBody(name = "Mars", position = np.array([-150.0, 0, 0]), velocity = np.array([0, 0, 5]), mass = 10, radius = 1)
        body_system.add_body(body)
    
    @staticmethod
    def __add_shuttle(body_system):
        body = ShuttleBody(name = "Shuttle", position = -50 * Vector.X(), velocity = -10 * Vector.Y(), mass = 1)
        body_system.add_body(body)