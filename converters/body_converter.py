import numpy as np
from models.bodies.sphere_body import SphereBody

class BodyConverter:
    @staticmethod
    def from_dictionary(dict):
        body_name = str(dict["body_name"])
        body_position = np.array(dict["body_position"])
        body_velocity = np.array(dict["body_velocity"])
        body_mass = float(dict["body_mass"])if "body_mass" in dict else 1
        body_radius = float(dict["body_radius"]) if "body_radius" in dict else 1
       
        body = SphereBody(name = body_name, position = body_position, velocity = body_velocity, mass = body_mass, radius = body_radius)
        return body