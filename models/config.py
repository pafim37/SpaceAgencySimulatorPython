class Config:
    def register_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_config(self)

    def set_configuration(self, data):
        self.show_coordinate_axes = data["show_coordinate_axes"]
        self.show_compass = data["show_compass"]
        self.show_orbits = data["show_orbits"]
        self.show_velocities = data["show_velocities"]
        self.movement = data["movement"]