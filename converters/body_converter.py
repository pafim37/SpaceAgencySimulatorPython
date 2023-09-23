import numpy as np
from models.bodies.sphere_body import SphereBody
from mathematica.vector import Vector

class BodyConverter:
    @staticmethod
    def from_dictionary(dict):
        body_name = str(dict["body_name"])
        position = dict["body_position"]
        velocity = dict["body_velocity"]
        body_position = Vector(position[0], position[1], position[2])
        body_velocity = Vector(velocity[0], velocity[1], velocity[2])
        body_mass = float(dict["body_mass"])if "body_mass" in dict else 1
        body_radius = float(dict["body_radius"]) if "body_radius" in dict else 1
       
        body = SphereBody(name = body_name, position = body_position, velocity = body_velocity, mass = body_mass, radius = body_radius)
        return body