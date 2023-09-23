import math 
import numpy as np
from ursina import *
from models.coordinate_axes import CoordinateAxes 
from models.bodies.body_type import BodyType
from mathematica.vector import Vector

class Body:
    def __init__(self, name, position, velocity, mass = 1, body_type = BodyType.UNDEFINED):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.center_body_name = "" # TODO: change that
        self.local_coordinate_system = CoordinateAxes(name, position)
        self.type = body_type
        self.t = 0
        self.has_orbit = False
        self.orbit = None

    def move(self, center_body):
        self.move_body(self, center_body)

    def get_relative_position_to(self, body):
        return self.position - body.position

    def get_relative_velocity_to(self, body):
        return self.velocity - body.velocity

    def get_sphere_of_influence_related_to(self, body):
        # TODO: Improve that
        distance = (self.position - body.position).magnitude()
        mass_ratio = math.pow(self.mass / body.mass, 0.4)
        return distance * mass_ratio

    def update(self, body):
        # TODO: update local_coordinate_system
        self.update_position(body.position)
        self.update_velocity(body.velocity)
        self.update_mass(body.mass)

    def update_position(self, position):
        self.position = position
    
    def update_velocity(self, velocity):
        self.velocity = velocity

    def update_mass(self, mass):
        self.mass = mass

    def update_center_body_name(self, name):
        self.center_body_name = name

    def move_analytic_body(self, focal_position):
        if self.has_orbit and self.name != "Shuttle":
            e = self.orbit.eccentricity
            T = self.orbit.period
            tp = self.orbit.perihelion_passage
            curr_ae = self.__calculate_eccentric_anomaly(e, T, tp) # self.orbit.direction * 
            curr_phi = 2 * math.atan(sqrt((1 + e) / (1 - e)) * math.tan(curr_ae/2))
            print("Curr_phi: ", self.name, math.degrees(curr_phi), math.degrees(self.orbit.true_anomaly) ) 
            print("orbit anges", math.degrees(self.orbit.orbit_phi), math.degrees(self.orbit.orbit_th))
            r = self.orbit.get_distance_from_focal_point(curr_phi)
            #####
            if self.orbit.orbit_th <= 0:
                x = r * math.cos(curr_phi) * math.cos(self.orbit.orbit_phi) + r * math.cos(curr_phi) * math.sin(self.orbit.orbit_th) 
            else:
                x = r * math.cos(curr_phi) * math.cos(self.orbit.orbit_phi) - r * math.cos(curr_phi) * math.sin(self.orbit.orbit_th) 
            y = r * math.sin(curr_phi)
            z = r * math.cos(curr_phi) * math.sin(self.orbit.orbit_th)
            self.position = Vector(x, y, z) + focal_position
            self.velocity = 2 * self.orbit.angular_momentum.cross(self.position) / self.position.magnitude()**2
            self.t += 0.1
            return
        else:
            # print(f"Can't move {self.name}")
            return    

    def __calculate_eccentric_anomaly(self, e, T, tp, tolerance=1e-4, max_iteration = 100):
        ae = 0
        L = ae - e * math.sin(ae) - 2 * math.pi * (self.t - tp) / T
        i = 0
        while abs(L) > tolerance:
            i += 1
            if i > max_iteration:
                return ae
            L = ae - e * math.sin(ae) - 2 * math.pi * (self.t - tp) / T
            dL = 1 - e * math.cos(ae)
            ae = ae - L/dL
        return ae

    def move_body(self, body, center_body):
        state = np.array([body.position[0], body.position[1], body.position[2], body.velocity[0], body.velocity[1], body.velocity[2]])
        state += self.runge_kutta_4(state, body, center_body)
        position = np.array([state[0], state[1], state[2]])
        velocity = np.array([state[3], state[4], state[5]])
        body.position = position
        body.velocity = velocity

    def runge_kutta_4(self, state, body, center_body):
        t = self.t
        h = 0.0001
        k1 = self.two_body_problem(t + h, state, body, center_body)
        k2 = self.two_body_problem(t + h/2, state + k1/2, body, center_body)
        k3 = self.two_body_problem(t + h/2, state + k2/2, body, center_body)
        k4 = self.two_body_problem(t + h, state + k3, body, center_body)
        state = (k1 + 2*k2 + 2*k3 + k4) / 6
        self.t += h
        return state
            
    def two_body_problem(self, t, state, body, center_body):
        position = np.array([state[0], state[1], state[2]])
        velocity = np.array([state[3], state[4], state[5]])
        relative_position = body.get_relative_position_to(center_body)
        relative_velocity = body.get_relative_velocity_to(center_body)
        r = np.linalg.norm(relative_position)
        force = -1 * body.mass * center_body.mass * relative_position / r**3 # TODO: return G
        a = force / body.mass
        new_position = velocity * t + 0.5 * a * t**2
        new_velocity = a * t
        return np.array([new_position[0], new_position[1], new_position[2], new_velocity[0], new_velocity[1], new_velocity[2]])
