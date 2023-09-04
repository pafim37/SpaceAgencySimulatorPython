import ursina as urs
import numpy as np
import math

class EntityConverter:
    @staticmethod
    def from_compass():
        arrow_x = urs.Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), color=urs.color.blue)
        arrow_y = urs.Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), rotation=(0, 0, -90), color=urs.color.green)
        arrow_z = urs.Entity(model="arrow", scale=(0.5,0.5,0.5), position=(3,1.5,0), rotation=(0, -90, 0), color=urs.color.red)
        return [arrow_x, arrow_y, arrow_z]

    @staticmethod
    def from_body(body, parent):
        body_entity = urs.Entity(parent=parent, model="sphere", name = f"{body.name}_body_entity", position = body.position / 100, scale = body.radius / 10)
        color = EntityConverter.__get_body_color(body.name)
        if isinstance(color, str):
            body_entity.texture = color
        else:
            body_entity.color = color
        return body_entity

    @staticmethod
    def from_body_velocity(body, parent):
        if not np.any(body.velocity):
            return None
        velocity_vector_entity = urs.Entity(parent=parent, model="arrow", name = f"{body.name}_velocity_entity", position = body.position / 100, scale = (3 * body.radius / 10, 0.1, 0.1), color = urs.color.white)
        vector_start = (1, 0, 0)
        vector_end = body.velocity
        d = np.dot(vector_start, vector_end)
        w = np.cross(vector_start, vector_end)
        q = urs.Quat(d + math.sqrt(d*d + np.dot(w, w)), w[0], w[1], w[2])
        velocity_vector_entity.quaternion = q / np.linalg.norm(q)
        return velocity_vector_entity

    @staticmethod
    def from_orbit(orbit, parent):
        return urs.Entity(parent=parent, model = urs.Mesh(vertices = orbit.points, mode='line'), name = f"{orbit.name}_orbit_entity", color = urs.color.blue)

    @staticmethod
    def __get_body_color(body_name):
        if body_name == "Earth":
            return "images/earth.jpg"
        elif body_name == "Jupiter":
            return "images/jupiter.jpg"
        elif body_name == "Mars":
            return "images/mars.jpg"
        elif body_name == "Neptune":
            return "images/neptune.jpg"
        elif body_name == "Saturn":
            return "images/saturn.jpg"
        elif body_name == "Sun":
            return "images/sun.jpg"
        elif body_name == "Uranus":
            return "images/uranus.jpg"
        elif body_name == "Venus":
            return "images/venus.jpg"
        elif body_name == "Mercury":
            return "images/mercury.jpg"
        elif body_name == "Moon":
            return "images/moon.jpg"
        else:
            return color.red