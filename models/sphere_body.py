from ursina import color
from models.body import Body

class SphereBody(Body):
    def __init__(self, name, position, velocity, mass = 1, radius = 1, color = color.red):
        super().__init__(name = name, position = position, velocity = velocity, mass = mass, color = color)
        self.radius = radius