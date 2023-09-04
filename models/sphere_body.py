from ursina import color
from models.body import Body

class SphereBody(Body):
    def __init__(self, name, position, velocity, mass = 1, radius = 1):
        super().__init__(name = name, position = position, velocity = velocity, mass = mass)
        self.radius = radius

    def update(self, body):
        super().update(body)
        self.update_radius(body.radius)

    def update_radius(self, radius):
        self.radius = radius