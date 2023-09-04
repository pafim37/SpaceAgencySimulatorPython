import ursina as urs
import time
import math
import numpy as np
from models.coordinate_axes import CoordinateAxes
from models.compass import Compass
from converters.entity_converter import EntityConverter

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
        self.player = urs.Entity(parent=self.group, model="images\shuttle.obj", texture="shuttle.png", position = (0, 0, 0), velocity = (0, 0, 0), scale = 0.0001 )
        self.player_velocity = (0, 0, 0)

    def __setup_camera(self):
        self.camera.position = (5, 5, -5)
        self.camera.rotation = (35, -45, 0)
 
    def __setup_window(self):
        urs.window.title = 'Space Agency Simulator'
        urs.window.borderless = False           
        urs.window.fullscreen = False               
        urs.window.exit_button.visible = True      
        urs.window.fps_counter.enabled = False   

    def update(self):
        self.__handle_keys()
        self.update_compass()
        self.group.rotation_z += urs.mouse.velocity[1] * urs.mouse.left * 150
        self.group.rotation_y -= urs.mouse.velocity[0] * urs.mouse.right * 150
        self.root.step()

    def __setup_compass(self):
        self.compass = Compass()
        self.compass_entities = self.compass.get_entities()

    def __setup_coordinate_axes(self):
        # TODO: fix bug with "UPDATE" body
        self.coordinate_axes = CoordinateAxes("Global Origin", np.array([0, 0, 0]), scale=1)
        self.coordinate_axes_entities = self.coordinate_axes.get_entities()

    def update_compass(self):
        if self.compass.enabled:
            self.compass.update(self.compass_entities, self.camera)

    def configure_compass(self, enabled):
        for entity in self.compass_entities:
            entity.enabled = enabled
    
    def configure_coordinate_axes(self):
        for entity in self.coordinate_axes_entities:
            entity.enabled = self.config.show_coordinate_axes
        for entity in self.__bodies_coordinate_system_entities:
            entity.enabled = self.config.show_coordinate_axes

    def configure_orbits(self, enabled):
        for entity in self.__orbits_entities:
            entity.enabled = enabled

    def configure_velocities(self, enabled):
        for entity in self.__velocities_entities:
            entity.enabled = enabled

    def register_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_urs_form(self)

    def synchronize_bodies_and_orbits(self, bodies, orbits):
        self.__synchronize_bodies(bodies)
        self.__synchronize_orbits(orbits)

    def __synchronize_bodies(self, bodies):
        for body_entity in self.__bodies_entities:
            urs.destroy(body_entity)
        for body_coordinate_system_entity in self.__bodies_coordinate_system_entities:
            urs.destroy(body_coordinate_system_entity)
        for velocity_entity in self.__velocities_entities:
            urs.destroy(velocity_entity) 
        self.__bodies_entities = []
        self.__bodies_coordinate_system_entities = []
        self.__velocities_entities = []
        for body in bodies:
            entity = EntityConverter.from_body(body=body, parent=self.group)
            self.__bodies_entities.append(entity)
            velocity_entity = EntityConverter.from_body_velocity(body=body, parent=self.group)
            if velocity_entity is not None:
                velocity_entity.enabled = self.config.show_velocities
                self.__velocities_entities.append(velocity_entity)
            entities = body.local_coordinate_system.get_entities()
            self.__bodies_coordinate_system_entities.extend(entities)
            for e in entities:
                e.parent = self.group
        self.configure_coordinate_axes()

    def __synchronize_orbits(self, orbits):
        for orbit_entity in self.__orbits_entities:
            urs.destroy(orbit_entity)
        self.__orbits_entities = []
        for orbit in orbits:
            entity = EntityConverter.from_orbit(orbit=orbit, parent=self.group)
            entity.enabled = self.config.show_orbits
            self.__orbits_entities.append(entity)

    def update_body_and_orbit(self, body, orbit):
        for body_entity in self.__bodies_entities:
            if body.name in body_entity.name:
                self.__bodies_entities.remove(body_entity)
                urs.destroy(body_entity)
                break
        for velocity_entity in self.__velocity_entities:
            if body.name in velocity_entity.name:
                self.__velocity_entities.remove(velocity_entity)
                urs.destroy(velocity_entity)
                break
        for orbit_entity in self.__orbits_entities:
            if body.name in orbit_entity.name:
                self.__orbits_entities.remove(orbit_entity)
                urs.destroy(orbit_entity)
                break
                
        body_entity = EntityConverter.form_body(body)
        self.__bodies_entities.append(body_entity)
        velocity_entity = EntityConverter.from_body_velocity(body=body, parent=self.group)
        if velocity_entity is not None:
            self.__velocities_entities.append(velocity_entity)
        if orbit is not None:
            orbit_entity = EntityConverter.from_orbit(orbit=orbit, parent=self.group)
            orbit_entity.enabled = self.config.show_orbits
            self.__orbits_entities.append(orbit_entity)
 
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
            
        if urs.held_keys['p']:
            print(self.camera.position)
            print(self.camera.rotation)

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