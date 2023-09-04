import math 
import numpy as np
from ursina import *
from models.coordinate_axes import CoordinateAxes 

class Body:
    def __init__(self, name, position, velocity, mass = 1):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.center_body_name = "" # TODO: change that
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

    def update(self, body):
        # TODO: update local_coordinate_system
        self.update_position(body.position)
        self.update_velocity(body.velocity)
        self.update_mass(body.mass)

    def update_position(self, position):
        self.position = position
    
    def update_velocity(self, velocity):
        self.velocity = velocity

    def update_mass(self, mass):
        self.mass = mass

    def update_center_body_name(self, name):
        self.center_body_name = name

    