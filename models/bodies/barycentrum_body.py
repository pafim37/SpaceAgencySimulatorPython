from models.bodies.body import Body
from models.bodies.body_type import BodyType

class BarycentrumBody(Body):
    def __init__(self, position, velocity, mass = 1):
        super().__init__(name = "Barycentrum", position = position, velocity = velocity, mass = mass, body_type = BodyType.BARYCENTRUM)

    def update(self, body):
        super().update(body)