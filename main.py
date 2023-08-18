from models.orbit import Orbit
import numpy as np
import math
from ursina import *
from models.compass import Compass
from models.body_system import BodySystem
from models.body import Body
from models.reference_system import ReferenceSystem
import time
import quaternion
import tkinter as tk
from tk_form import TkForm
from mediator import Mediator
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  
    ]
)

def update():
    # synchronize body and orbit
    if not mediator.is_body_system_synchronize_with_entities:
        logging.info("Starting synchronize bodies and orbits")
        global entities
        for entity in entities:
            destroy(entity)
        
        entities = []
        for body in body_system.get_bodies():
            entities.append(convert_body_to_entity(body))
        for orbit in body_system.get_orbits():
            entities.append(convert_orbit_to_entity(orbit))
        mediator.is_body_system_synchronize_with_entities = True
        logging.info("Ending synchronize body and orbit")

    # handle keys
    __handle_keys()

    # update compass
    compass.update(compass_arrow_entities, camera)

    # show coordinate system axes
    coordinate_system_axis_x.enabled = mediator.show_coordinate_axes
    coordinate_system_axis_y.enabled = mediator.show_coordinate_axes
    coordinate_system_axis_z.enabled = mediator.show_coordinate_axes

    for arrow in compass_arrow_entities:
        arrow.enabled = mediator.show_compass

    tk_form.update_root()

# create tkinter
tk_form = TkForm()

# create urisina app
app = Ursina()
Sky(texture="nig-sky1.jpg")
# config window
window.title = 'Space Agency Simulator'
window.borderless = False           
window.fullscreen = False               
window.exit_button.visible = True      
window.fps_counter.enabled = False   


# global position
OX, OY, OZ = 0, 0, 0
one_vector = True
# camera
camera.position = (5, 5, -5)
camera.rotation = (35, -45, 0)

# body system
body_system = BodySystem(G = 1)
entities = []

compass = Compass()
compass_arrow_entities = compass.get_entities()

# mediator
mediator = Mediator()
mediator.camera = camera
mediator.body_system = body_system
tk_form.register_mediator(mediator)
tk_form.send_configuration()

# coordinate system axes
coordinate_system_axis_x = Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), color=color.blue)
coordinate_system_axis_y = Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), rotation=(0,0,-90), color=color.green)
coordinate_system_axis_z = Entity(model="arrow", scale=(10,0.2,0.2), position=(0,0,0), rotation=(0,-90,0), color=color.red)

def convert_body_to_entity(body):
    body_entity = Entity(model="sphere", name = f"{body.name}_body_entity", position = body.position / 100, scale = body.radius / 10, color = body.color)
    if body.name == "Sun":
        body_entity.texture = "sun.jpg"
    elif body.name == "Earth":
        body_entity.texture = "earth.jpg"

    return body_entity

def convert_orbit_to_entity(orbit):
    tcolor = color.blue
    if orbit.name == "test2":
        tcolor = color.green
    return Entity(model = Mesh(vertices = orbit.points, mode='line'), name = f"{orbit.name}_orbit_entity", color = tcolor)

def convert_velocity_to_entity(body):
    arrow = body.velocity
    arrow = __normalize(arrow)
    rs = ReferenceSystem((0,0,0), arrow)
    position = np.array(body.position / 100) + np.array([0.25 * arrow[0], 0.25 * arrow[1], 0.25 * arrow[2]])
    return Entity(model = "arrow", name = f"{body.name}_velocity_entity", rotation = (90, - math.degrees(rs.th), -math.degrees(rs.phi)), color = color.white, position = body.position / 100, scale = (0.5, 0.2, 0.2))

def __normalize(vector):
        if np.linalg.norm(vector) == 0:
            return np.array([0,0,0])
        else:
            return vector / np.linalg.norm(vector)

def __handle_keys():
    global OX, OY, OZ
    if held_keys['c']:
        camera.rotation_x += 0.5

    if held_keys['v']:
        camera.rotation_x -= 0.5

    if held_keys['e']:
        camera.rotation_y += 0.5

    if held_keys['q']:
        camera.rotation_y -= 0.5

    if held_keys['z']:
        camera.rotation_z += 0.5

    if held_keys['x']:
        camera.rotation_z -= 0.5

    if held_keys['right arrow']:
        camera.position += (0.1, 0, 0)

    if held_keys['up arrow']:
        camera.position += (0, 0.1, 0)

    if held_keys['w']:
        camera.position += (0, 0, 0.1)

    if held_keys['left arrow']:
        camera.position += (-0.1, 0, 0)

    if held_keys['down arrow']:
        camera.position += (0, -0.1, 0)

    if held_keys['s']:
        camera.position += (0, 0, -0.1)
        
    if held_keys['h']:
        OX += 1
        print(OX, OY, OZ)

    if held_keys['b']:
        OX -= 1
        print(OX, OY, OZ)

    if held_keys['k']:
        OZ += 1
        print(OX, OY, OZ)
    if held_keys['m']:
        OZ -= 1
        print(OX, OY, OZ)

    if held_keys['j']:
        OY += 1
        print(OX, OY, OZ)

    if held_keys['n']:
        OY -= 1
        print(OX, OY, OZ)

    if held_keys['l']:
        OX, OY, OZ = 0, 0, 0

    if held_keys['i']:
        orbits = body_system.get_orbits()
        for orbit in orbits:
            print(orbit)

    if held_keys['p']:
        print(camera.position)
        print(camera.rotation)

app.run()

