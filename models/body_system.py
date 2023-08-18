import math
from models.body import Body
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

    def add_body(self, body):
        if any(b.name == body.name for b in self.__bodies):
            raise BodyAlreadyExistsException(body)
        else:
            self.__bodies.append(body)
            self.__update()

    def add_or_remove(self, body):
        if any(b.name == body.name for b in self.__bodies):
            logging.info(f"Removing {body.name} from body system")
            self.remove_body_by_name(body.name)
        else:
            logging.info(f"Adding {body.name} to body system")
            self.add_body(body)

    def add_or_update(self, body):
        for b in self.__bodies:
            if b.name == body.name:
                self.remove_body_by_name(body.name)
                break
        logging.info(f"Adding or updating {body.name} to body system, number of bodies: {len(self.__bodies)} ")
        self.add_body(body)
        logging.info(f"Adding or updating {body.name} to body system, number of bodies: {len(self.__bodies)} ")

    def add_body_from_dict(self, dict):
        logging.debug(f"Creating body from dict {dict}")
        body_name = str(dict["body_name"])
        body_position = np.array(dict["body_position"])
        body_velocity = np.array(dict["body_velocity"])
        body_mass = np.array(dict["body_mass"])if "body_mass" in dict else 1
        body_radius = np.array(dict["body_radius"]) if "body_radius" in dict else 1
        body_color = dict["body_color"] if "body_color" in dict else color.red
        body = Body(name = body_name, position = body_position, velocity = body_velocity, mass = body_mass, radius = body_radius, color = body_color)
        self.add_or_update(body)
        return body, self.get_orbit_by_name(body.name)

    def remove_body(self, body):
        self.__bodies.remove(body)
        self.__update()

    def remove_body_by_name(self, name):
        for body in self.__bodies:
            if body.name == name:
                self.remove_body(body)

    def remove_orbit_by_name(self, name):
        for orbit in self.__orbits:
            if name in orbit.name:
                self.__orbits.remove(orbit)

    def get_body_by_name(self, name):
        for body in self.__bodies:
            if body.name == name:
                return body

    def get_orbit_by_name(self, name):
        for orbit in self.__orbits:
            if orbit.name == name:
                return orbit

    def get_bodies(self):
        return self.__bodies

    def get_orbits(self):
        return self.__orbits

    def add_or_remove_sun(self):
        body = Body(name = "Sun", position = np.zeros(3), velocity = np.zeros(3), mass = 10000, radius = 2, color = "images/sun.jpg")
        self.add_or_remove(body)

    def add_or_remove_earth(self):
        body = Body(name = "Earth", position = np.array([50, 0, 0]), velocity = np.array([0, 17, 0]), mass = 10, radius = 1, color = "images/earth.jpg")
        self.add_or_remove(body)

    def add_or_remove_mars(self):
        body = Body(name = "Mars", position = np.array([150, 0, 0]), velocity = np.array([0, 5, 0]), mass = 10, radius = 1, color = "images/mars.jpg")
        self.add_or_remove(body)

    def register_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_body_system(self)

    def __update(self):
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
            self.barycentrum = Body(self.__barycentrum_name, np.zeros(3), np.zeros(3), total_mass, 0)
        else:
            position = 1 / total_mass * sum(body.mass * body.position for body in self.__bodies)
            self.barycentrum = Body(self.__barycentrum_name, position, np.zeros(3), total_mass, 0)

    def __find_orbits(self):
        logging.info("Finding orbits")
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

    def __str__(self):
        output = ""
        for body in self.__bodies:
            output += str(body)
        for orbit in self.__orbits:
            output += str(orbit)
        return output