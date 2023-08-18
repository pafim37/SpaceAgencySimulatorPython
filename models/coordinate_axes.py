import ursina as urs

class CoordinateAxes:
    def __init__(self):
        self.enabled = True

    def get_entities(self):
        coordinate_system_axis_x = urs.Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), color=urs.color.blue)
        coordinate_system_axis_y = urs.Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), rotation=(0,0,-90), color=urs.color.green)
        coordinate_system_axis_z = urs.Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), rotation=(0,-90,0), color=urs.color.red)
        return [coordinate_system_axis_x, coordinate_system_axis_y, coordinate_system_axis_z]
