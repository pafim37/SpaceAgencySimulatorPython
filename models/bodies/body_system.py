import math
from models.bodies.barycentrum_body import BarycentrumBody
from models.orbits.orbit import Orbit
import numpy as np
import time
import sys
import logging
from ursina import color
np.set_printoptions(suppress=True)
class BodySystem:
    def __init__(self, G = 6.674301515 * math.pow(10, -11)):
        self.__bodies = []
        self.__u = 0
        self.__G = G
        self.__barycentrum_name = "Barycentrum"
        self.barycentrum = None
        self.calibrate_barycentrum = False
        self.t = 0
        self.movement = False

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

    def update(self):
        self.__bodies.sort(key=lambda x: x.mass)
        self.__update_u()
        self.__update_barycentrum()
        if len(self.__bodies) > 1:
            self.__find_orbits()
        if self.movement:
            self.update_shuttle()
            # self.move_planets()

    def get_player(self):
        return self.get_body_by_name("Shuttle")

    def update_shuttle(self):
        shuttle = self.get_body_by_name("Shuttle")
        center_body = self.get_body_by_name(shuttle.center_body_name)
        shuttle.move()

    def thrust_shuttle(self, v):
        shuttle = self.get_body_by_name("Shuttle")
        shuttle.thurst(v)

    def __update_u(self): 
        total_mass = sum(body.mass for body in self.__bodies)
        self.__u = self.__G * total_mass

    def __update_barycentrum(self): 
        total_mass = sum(body.mass for body in self.__bodies)
        if total_mass == 0:
            self.barycentrum = BarycentrumBody(position = np.zeros(3), velocity = np.zeros(3), mass = total_mass)
        else:
            position = 1 / total_mass * sum(body.mass * body.position for body in self.__bodies)
            self.barycentrum = BarycentrumBody(position = position, velocity = np.zeros(3), mass = total_mass)
        if self.calibrate_barycentrum:
            for body in self.__bodies:
                body.position -= self.barycentrum.position
            self.barycentrum.position -= self.barycentrum.position

    def __find_orbits(self):
        logging.info("Finding orbits")
        # TODO: is it needed?
        for body in self.__bodies: 
            body.center_body_name = ""
            body.orbit = None
            body.has_orbit = False
        for i in range(len(self.__bodies) - 1):
            curr_body = self.__bodies[i]
            print()
            distance = sys.float_info.max
            for j in range(i+1, len(self.__bodies)):
                center_body = self.__bodies[j]
                if curr_body.mass / center_body.mass > 0.03: # TODO: extract this value
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
                curr_body.orbit = orbit
                curr_body.has_orbit = True
        self.__bodies[-1].center_body_name = self.barycentrum.name