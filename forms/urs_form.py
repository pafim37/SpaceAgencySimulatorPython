import ursina as urs
import time
import math
import numpy as np
from models.coordinate_axes import CoordinateAxes
from models.compass import Compass
from converters.entity_converter import EntityConverter
from models.bodies.body_type import BodyType
from mediator.commands import *
import time

class UrsForm:
    def __init__(self):
        self.root = urs.Ursina()
        urs.Sky(texture="images/stars.jpg")
        self.camera = urs.camera
        self.__setup_window()
        self.__setup_camera()
        self.__setup_compass()
        self.__setup_coordinate_axes()
        self.__bodies_entities = []
        self.__velocities_entities = []
        self.__bodies_coordinate_system_entities = []
        self.__orbits_entities = []
        self.group = urs.Entity()
        self.shuttle_rotation = urs.Entity(parent=self.group)
        self.player_entity = None
        self.start = time.time()

    def __setup_camera(self):
        self.camera.position = (5, 5, -5)
        self.camera.rotation = (35, -45, 0)
 
    def __setup_window(self):
        urs.window.title = 'Space Agency Simulator'
        urs.window.borderless = False           
        urs.window.fullscreen = False               
        urs.window.exit_button.visible = True      
        urs.window.fps_counter.enabled = False   

    def assign_player(self):
        self.player_entity = EntityConverter.from_body(body=self.mediator.send(Command.GET_PLAYER), parent=self.shuttle_rotation)

    def update(self):
        self.update_player()
        self.__handle_keys()
        self.update_compass()
        self.root.step()

    def update_player(self):
        player = self.mediator.send(Command.GET_PLAYER)
        self.shuttle_rotation.rotation = (0, 0, 0)
        self.shuttle_rotation.world_rotation = (0, 0, 0)
        self.player_entity.rotation = (0, 0, 0)
        self.shuttle_rotation.rotation_x = player.angle_x
        self.shuttle_rotation.rotation_y = player.angle_y
        self.shuttle_rotation.rotation_z = player.angle_z
        self.player_entity.rotation = self.player_entity.world_rotation
        self.shuttle_rotation.rotation = (0, 0, 0)
        self.player_entity.position = player.position / 100

    def __setup_compass(self):
        self.compass = Compass()
        self.compass_entities = EntityConverter.from_compass()

    def __setup_coordinate_axes(self):
        # TODO: fix bug with "UPDATE" body
        self.coordinate_axes = CoordinateAxes("Global Origin", np.array([0, 0, 0]), scale=1)
        self.coordinate_axes_entities = EntityConverter.from_coordinate_axes(self.coordinate_axes)

    def update_compass(self):
        if self.compass.enabled:
            new_arrow_position = self.compass.update(self.camera)
            for arrow in self.compass_entities:
                arrow.position = new_arrow_position

    def configure_compass(self, enabled):
        self.compass.enabled = enabled
        for entity in self.compass_entities:
            entity.enabled = enabled
    
    def configure_coordinate_axes(self):
        for entity in self.coordinate_axes_entities:
            entity.enabled = self.config.show_coordinate_axes
        for entity in self.__bodies_coordinate_system_entities:
            entity.enabled = self.config.show_coordinate_axes

    def configure_orbits(self, enabled):
        for orbit_entity in self.__orbits_entities:
            orbit_entity.enabled = enabled

    def configure_velocities(self, enabled):
        for velocity_entity in self.__velocities_entities:
            velocity_entity.enabled = enabled

    def register_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_urs_form(self)

    def synchronize_bodies(self, bodies):
        for body_entity in self.__bodies_entities:
            urs.destroy(body_entity)
        for body_coordinate_system_entity in self.__bodies_coordinate_system_entities:
            urs.destroy(body_coordinate_system_entity)
        for velocity_entity in self.__velocities_entities:
            urs.destroy(velocity_entity)
        for orbit_entity in self.__orbits_entities:
            urs.destroy(orbit_entity)
        self.__orbits_entities = []
        self.__bodies_entities = []
        self.__bodies_coordinate_system_entities = []
        self.__velocities_entities = []
        for body in bodies:
            if body.type == BodyType.SPHERE:
                entity = EntityConverter.from_body(body=body, parent=self.group)
                self.__bodies_entities.append(entity)
                velocity_entity = EntityConverter.from_body_velocity(body=body, parent=self.group)
                if velocity_entity is not None:
                    velocity_entity.enabled = self.config.show_velocities
                    self.__velocities_entities.append(velocity_entity)
                entities = EntityConverter.from_coordinate_axes(body.local_coordinate_system)
                self.__bodies_coordinate_system_entities.extend(entities)
                if body.has_orbit:
                    orbit_entity = EntityConverter.from_orbit(orbit=body.orbit, parent=self.group)
                    orbit_entity.enabled = self.config.show_orbits
                    self.__orbits_entities.append(orbit_entity)
                for e in entities:
                    e.parent = self.group
        self.configure_coordinate_axes()

    def __handle_keys(self):
        if urs.held_keys['c']:
            self.camera.rotation_x += 0.5

        if urs.held_keys['v']:
            self.camera.rotation_x -= 0.5

        if urs.held_keys['e']:
            self.camera.rotation_y += 0.5

        if urs.held_keys['q']:
            self.camera.rotation_y -= 0.5

        if urs.held_keys['z']:
            self.camera.rotation_z += 0.5

        if urs.held_keys['x']:
            self.camera.rotation_z -= 0.5

        if urs.held_keys['right arrow']:
            self.camera.position += (0.1, 0, 0)

        if urs.held_keys['up arrow']:
            self.camera.position += (0, 0.1, 0)

        if urs.held_keys['w']:
            self.camera.position += (0, 0, 0.1)

        if urs.held_keys['left arrow']:
            self.camera.position += (-0.1, 0, 0)

        if urs.held_keys['down arrow']:
            self.camera.position += (0, -0.1, 0)

        if urs.held_keys['s']:
            self.camera.position += (0, 0, -0.1)

        if urs.held_keys['t']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_x_p")

        if urs.held_keys['y']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_x_m")

        if urs.held_keys['u']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_y_p")

        if urs.held_keys['i']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_y_m")

        if urs.held_keys['o']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_z_p")

        if urs.held_keys['p']:
            self.mediator.send(Command.THRUST_PLAYER, "rotate_z_m")
        
        if urs.held_keys['r']:
            self.angle_x = 0
            self.angle_y = 0
            self.angle_z = 0
            self.player_velocity = urs.Vec3(0, 0, 0)
            self.shuttle_rotation.rotation = (0, 0, 0)
            self.shuttle_rotation.world_rotation = (0, 0, 0)
            self.player_entity.rotation = (0, 0, 0)
            self.player_entity.position = (0, 0, 0)

        if urs.held_keys['p']:
            print(self.camera.position)
            print(self.camera.rotation)

        if not urs.held_keys["space"]:
            self.key_pressed = False

        if urs.held_keys['space'] and not self.key_pressed:
            v = 0.01 * self.player_entity.right / np.linalg.norm(self.player_entity.right) 
            self.mediator.send(Command.THRUST_PLAYER, v)
            self.key_pressed = True

    def set_configuration(self, config):
        # TODO: consider self.config when adding new orbit
        self.config = config
        self.configure_compass(config.show_compass)
        self.configure_coordinate_axes()
        self.configure_orbits(config.show_orbits)
        self.configure_velocities(config.show_velocities)

    def go_home_camera(self):
        self.camera.position = (5, 5, -5)
        self.camera.rotation = (35, -45, 0)

    def set_position_ox_camera(self):
        self.camera.position = (-10, 0, 0)
        self.camera.rotation = (0, 90, -90)    

    def set_position_oy_camera(self):
        self.camera.position = (0, 10, 0)
        self.camera.rotation = (90, 0, 0)

    def set_position_oz_camera(self):
        self.camera.position = (0, 0, -10)
        self.camera.rotation = (0, 0, 0)

    def set_position_camera(self, entity_name):
        entity = next((e for e in self.__bodies_entities if entity_name in e.name), None)
        position = entity.position
        d_position = entity.position
        for e in self.__bodies_entities:
            e.position -= d_position
        for v in self.__velocities_entities:
            v.position -= d_position
        for o in self.__orbits_entities:
            o.position -= d_position
        for s in self.__bodies_coordinate_system_entities:
            s.position -= d_position

if __name__=="__main__":
    app = UrsForm()
    start = time.time()
    while True:
        if time.time() - start > 15:
            break
        app.update()