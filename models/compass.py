import math
import numpy as np
from ursina import *

class Compass():
    def __init__(self):
        self.enabled = True

    def get_entities(self):
        arrow_x = Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), color=color.blue)
        arrow_y = Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), rotation=(0, 0, -90), color=color.green)
        arrow_z = Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), rotation=(0, -90, 0), color=color.red)
        return [arrow_x, arrow_y, arrow_z]

    def update(self, arrows, camera):
        x = math.radians(camera.rotation[0])
        y = math.radians(camera.rotation[1])
        z = math.radians(camera.rotation[2])
        for arrow in arrows:
            arrow.position = self.__rotation_matrix_y(y) @ self.__rotation_matrix_x(x) @ self.__rotation_matrix_z(z) @ (3,1.5,10) + camera.position
            arrow.position = self.__rotation_matrix_y(y) @ self.__rotation_matrix_x(x) @ self.__rotation_matrix_z(z) @ (3,1.5,10) + camera.position
            arrow.position = self.__rotation_matrix_y(y) @ self.__rotation_matrix_x(x) @ self.__rotation_matrix_z(z) @ (3,1.5,10) + camera.position
    
    def __rotation_matrix_z(self, yaw):
        cos = np.cos(yaw)
        sin = np.sin(yaw)
        return np.array([
            [cos, sin, 0],
            [-sin, cos, 0],
            [0, 0, 1]
        ])

    def __rotation_matrix_y(self, pitch):
        cos = np.cos(pitch)
        sin = np.sin(pitch)
        return np.array([
            [cos, 0, sin],
            [0, 1, 0],
            [-sin, 0, cos]
        ])

    def __rotation_matrix_x(self, roll):
        cos = np.cos(roll)
        sin = np.sin(roll)
        return np.array([
            [1, 0, 0],
            [0, cos, -sin],
            [0, sin, cos]
        ])
