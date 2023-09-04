import math
from models.bodies.body import Body
from models.bodies.sphere_body import SphereBody
from models.orbit import Orbit
import numpy as np
import sys
import logging
from exceptions.body_already_exists_exception import BodyAlreadyExistsException
from ursina import color

class BodySystem:
    def __init__(self, G = 6.674301515 * math.pow(10, -11)):
        self.__bodies = []
        self.__orbits = []
        self.__u = 0
        self.__G = G
        self.__barycentrum_name = "Barycentrum"
        self.barycentrum = None
        self.shuttle = None
        self.calibrate_barycentrum = False
        self.__add_planets()

    def add_or_update_body(self, body):
        for b in self.__bodies:
            if body.name == b.name:
                b.update(body)
                return
        self.add_body(body)

    def register_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_body_system(self)
    
    def add_body(self, body):
        self.__bodies.append(body)

    def remove_body(self, body):
        self.__bodies.remove(body)

    def remove_body_by_name(self, name):
        for body in self.__bodies:
            if body.name == name:
                self.remove_body(body)

    def get_body_by_name(self, name):
        return next((body for body in self.__bodies if body.name == name), None)

    def get_bodies(self):
        return self.__bodies

    def get_orbits(self):
        return self.__orbits

    def update(self):
        self.__bodies.sort(key=lambda x: x.mass)
        self.__update_u()
        self.__update_barycentrum()
        if len(self.__bodies) > 1:
            self.__find_orbits()
        else:
            self.__orbits = []

    def __update_u(self): 
        total_mass = sum(body.mass for body in self.__bodies)
        self.__u = self.__G * total_mass

    def __update_barycentrum(self): 
        total_mass = sum(body.mass for body in self.__bodies)
        if total_mass == 0:
            self.barycentrum = SphereBody(name = self.__barycentrum_name, position = np.zeros(3), velocity = np.zeros(3), mass = total_mass, radius = 0)
        else:
            position = 1 / total_mass * sum(body.mass * body.position for body in self.__bodies)
            self.barycentrum = SphereBody(name = self.__barycentrum_name, position = position, velocity = np.zeros(3), mass = total_mass, radius = 0)
        if self.calibrate_barycentrum:
            for body in self.__bodies:
                body.position -= self.barycentrum.position
            self.barycentrum.position -= self.barycentrum.position

    def __find_orbits(self):
        logging.info("Finding orbits")
        for body in self.__bodies:
            body.center_body_name = ""
        self.__orbits = []
        for i in range(len(self.__bodies) - 1):
            curr_body = self.__bodies[i]
            distance = sys.float_info.max
            for j in range(i+1, len(self.__bodies)):
                center_body = self.__bodies[j]
                if curr_body.mass / center_body.mass > 0.03:
                    continue
                relative_distance = np.linalg.norm(curr_body.get_relative_position_to(center_body))
                influence = center_body.get_sphere_of_influence_related_to(curr_body)
                if (relative_distance < distance and influence >= relative_distance):
                    distance = relative_distance
                    curr_body.center_body_name = center_body.name
            if curr_body.center_body_name != "" and curr_body.center_body_name != "Barycentrum": # TODO: do sth with that
                center_body = self.get_body_by_name(curr_body.center_body_name)
                u = self.__G * (curr_body.mass + center_body.mass)
                orbit = Orbit(curr_body, center_body, u)
                self.__orbits.append(orbit)
        self.__bodies[-1].center_body_name = self.barycentrum.name



    def __add_planets(self):
        self.__add_sun()
        self.__add_earth() 
        self.__add_moon() 
        self.__add_mars()
        # self.__add_jupiter()
        # self.__add_neptune()

    # def __add_sun(self):
    #     body = SphereBody(name = "Sun", position = np.array([0, 0, 0], dtype=float), velocity = np.zeros(3), mass = 2 * math.pow(10, 30), radius = 10, color = "images/sun.jpg")
    #     self.add_body(body)

    # def __add_earth(self):
    #     body = SphereBody(name = "Earth", position = np.array([1.5 * math.pow(10, 11), 0, 0]), velocity = np.array([0, 28000, 0]), mass = 6 * math.pow(10, 24), radius = 2, color = "images/earth.jpg")
    #     self.add_body(body)

    # def __add_moon(self):
    #     body = SphereBody(name = "Moon", position = np.array([1.5038 * math.pow(10, 11), 0, 0], dtype=float), velocity = np.array([0, 30000, 0]), mass = 7.3 * math.pow(10, 22), radius = 1, color = "images/moon.jpg")
    #     self.add_body(body)

    # def __add_mars(self):
    #     body = SphereBody(name = "Mars", position = np.array([2.2792 * math.pow(10, 11), 0, 0]), velocity = np.array([0, 5, 0]), mass = 6.4 * math.pow(10, 23), radius = 1, color = "images/mars.jpg")
    #     self.add_body(body)

    # def __add_jupiter(self):
    #     body = SphereBody(name = "Jupiter", position = np.array([7.7857 * math.pow(10, 11) , 0, 0]), velocity = np.array([0, 5, 0]), mass = 1.9 * math.pow(10, 27), radius = 2, color = "images/jupiter.jpg")
    #     self.add_body(body)

    # def __add_neptune(self):
    #     body = SphereBody(name = "Neptune", position = np.array([4.49506 * math.pow(10, 12), 0, 0]), velocity = np.array([0, 5, 0]), mass = math.pow(10, 26), radius = 2, color = "images/neptune.jpg")
    #     self.add_body(body)

    def __add_sun(self):
        body = SphereBody(name = "Sun", position = np.array([50.0, 0, 0]), velocity = np.zeros(3), mass = 10000, radius = 2)
        self.add_body(body)

    def __add_earth(self):
        body = SphereBody(name = "Earth", position = np.array([100.0, 0, 0]), velocity = np.array([0, 17, 0]), mass = 100, radius = 1)
        self.add_body(body)

    def __add_moon(self):
        body = SphereBody(name = "Moon", position = np.array([100.0, 10, 0]), velocity = np.array([0, 17, 3]), mass = 1, radius = 0.2)
        self.add_body(body)

    def __add_mars(self):
        body = SphereBody(name = "Mars", position = np.array([-150.0, 0, 0]), velocity = np.array([0, 0, 5]), mass = 10, radius = 1)
        self.add_body(body)