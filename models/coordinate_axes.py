import ursina as urs
import numpy as np

class CoordinateAxes:
    def __init__(self, name, origin, scale = 0.06):
        self.enabled = True
        self.origin = origin
        self.name = name
        self.ox = [1, 0, 0]
        self.oy = [0, 1, 0]
        self.oz = [0, 0, 1]
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        self.scale = scale

    def get_entities(self):
        print(self.origin)
        # TODO: consider scale
        scale = np.array([10 * self.scale, 0.2, 0.2])
        coordinate_system_axis_x = urs.Entity(model="arrow", name = self.name, scale=scale, position=self.origin / 100, color=urs.color.blue)
        coordinate_system_axis_y = urs.Entity(model="arrow", name = self.name, scale=scale, position=self.origin / 100, rotation=(0,0,-90), color=urs.color.green)
        coordinate_system_axis_z = urs.Entity(model="arrow", name = self.name, scale=scale, position=self.origin / 100, rotation=(0,-90,0), color=urs.color.red)
        return [coordinate_system_axis_x, coordinate_system_axis_y, coordinate_system_axis_z]