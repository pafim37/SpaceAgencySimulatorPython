from models.bodies.body import Body
from models.bodies.body_type import BodyType

class SphereBody(Body):
    def __init__(self, name, position, velocity, mass = 1, radius = 1):
        super().__init__(name = name, position = position, velocity = velocity, mass = mass, body_type = BodyType.SPHERE)
        self.radius = radius

    def update(self, body):
        super().update(body)
        self.update_radius(body.radius)

    def update_radius(self, radius):
        self.radius = radius