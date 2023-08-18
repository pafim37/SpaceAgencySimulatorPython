import math 
import numpy as np
from ursina import *

class Body:
    def __init__(self, name, position, velocity, mass = 1, radius = 1, color = color.red):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.center_body_name = ""
        self.texture = color
        self.color = color

    def get_relative_position_to(self, body):
        return self.position - body.position

    def get_sphere_of_influence_related_to(self, body):
        # TODO: Improve that
        distance = np.linalg.norm(self.position - body.position)
        mass_ratio = math.pow(self.mass / body.mass, 0.4)
        return distance * mass_ratio

    def __str__(self):
        return f"{self.name}: pos: {self.position}, vel: {self.velocity}, mass: {self.mass}, radius: {self.radius}, center_body_name: {self.center_body_name}\n"
