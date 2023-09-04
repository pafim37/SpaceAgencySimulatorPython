import ursina as urs
import numpy as np

class CoordinateAxes:
    def __init__(self, name, origin, scale = 0.06):
        self.enabled = True
        self.origin = origin
        self.name = name
        self.scale = scale
