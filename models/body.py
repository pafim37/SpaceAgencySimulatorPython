import math 
import numpy as np
from ursina import *
from models.coordinate_axes import CoordinateAxes 

class Body:
    def __init__(self, name, position, velocity, mass = 1, color = color.red):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.center_body_name = "" # TODO: change that
        self.texture = color
        self.color = color
        self.local_coordinate_system = CoordinateAxes(name, position)

    def get_relative_position_to(self, body):
        return self.position - body.position

    def get_relative_velocity_to(self, body):
        return self.velocity - body.velocity

    def get_sphere_of_influence_related_to(self, body):
        # TODO: Improve that
        distance = np.linalg.norm(self.position - body.position)
        mass_ratio = math.pow(self.mass / body.mass, 0.4)
        return distance * mass_ratio

    def __str__(self):
        return f"{self.name}: pos: {self.position}, vel: {self.velocity}, mass: {self.mass}, radius: {self.radius}, center_body_name: {self.center_body_name}\n"
