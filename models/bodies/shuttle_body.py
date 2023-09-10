from models.bodies.body import Body
from models.bodies.body_type import BodyType
import numpy as np

class ShuttleBody(Body):
    def __init__(self, name, position, velocity, mass = 1):
        super().__init__(name = name, position = position, velocity = velocity, mass = mass, body_type = BodyType.SHUTTLE)
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.rotation_velocity_x = 0
        self.rotation_velocity_y = 0
        self.rotation_velocity_z = 0
        self.speed = 0.01
        self.move_toward = np.array([0, 0, 0.0])

    def update(self, body):
        super().update(body)

    def move(self):
        self.position += self.move_toward
        self.angle_x += self.rotation_velocity_x
        self.angle_y += self.rotation_velocity_y
        self.angle_z += self.rotation_velocity_z
        return
        # super().move(center_body)

    def thurst(self, v):
        # TODO: refactor this
        if v == "rotate_x_p":
            self.rotation_velocity_x += 0.1
            return
        if v == "rotate_x_m":
            self.rotation_velocity_x -= 0.1
            return
        if v == "rotate_y_p":
            self.rotation_velocity_y += 0.1
            return
        if v == "rotate_y_m":
            self.rotation_velocity_y -= 0.1
            return
        if v == "rotate_z_p":
            self.rotation_velocity_z += 0.1
            return
        if v == "rotate_z_m":
            self.rotation_velocity_z -= 0.1
            return
        self.move_toward += v
        self.velocity += v
        