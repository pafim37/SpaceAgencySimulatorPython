import tkinter as tk
from mediator.commands import *
import math
from models.bodies.body_type import BodyType

class TkForm:
    def __init__(self):
        self.root = tk.Tk()
        self.__setup_root()
        self.__create_variables()
        self.__setup_frames()

    def register_mediator(self, mediator):
        self.mediator = mediator
        self.mediator.register_tk_form(self)

    def send_command(self, command):
        self.mediator.send(command)
    
    def send_command_with_data(self, command, data):
        self.mediator.send(command, data)

    def update(self):
        self.root.update()

    def update_with_synchronize_bodies(self, bodies):
        self.synchronize_bodies(bodies)
        self.update()

    def __setup_root(self):
        self.root.title("Setup panel")
        self.root.geometry("720x700")

    def __create_variables(self):
        self.body_name_var = tk.StringVar(self.root, "Venus")
        self.body_position_x_var = tk.DoubleVar(self.root, -75)
        self.body_position_y_var = tk.DoubleVar(self.root, -75)
        self.body_position_z_var = tk.DoubleVar(self.root, 0)
        self.body_velocity_x_var = tk.DoubleVar(self.root, 0)
        self.body_velocity_y_var = tk.DoubleVar(self.root, 5)
        self.body_velocity_z_var = tk.DoubleVar(self.root, 0)
        self.body_mass_var = tk.DoubleVar(self.root, 1)
        self.body_radius_var = tk.DoubleVar(self.root, 1)

        self.coordinate_axes_enabled_var  = tk.BooleanVar(self.root, False)
        self.compass_enabled_var = tk.BooleanVar(self.root, False)
        self.orbits_enabled_var = tk.BooleanVar(self.root, True)
        self.velocity_enabled_var = tk.BooleanVar(self.root, True)
        self.barycentrum_enabled_var = tk.BooleanVar(self.root, False)
        self.movement_var = tk.BooleanVar(self.root, False)

    def __setup_frames(self):
        body_frame = self.__setup_body_frame()
        configuration_frame = self.__setup_configuration_frame()
        camera_frame = self.__setup_camera_frame()
        self.body_info = self.__setup_body_info()
        
        body_frame.grid(row = 0, column = 0, padx = 10, pady=10)
        configuration_frame.grid(row = 1, column = 0, padx = 10, pady=10)
        camera_frame.grid(row = 2, column = 0, padx = 10, pady=10)
        self.body_info.grid(row = 0, column = 1, padx = 10, pady = 10, rowspan = 4, sticky=tk.N)


    def __setup_body_frame(self):
        setup_body_lf = tk.LabelFrame(self.root, text="Body Setup")

        tk.Label(setup_body_lf, text="Name").grid(row = 0, column = 0)
        tk.Entry(setup_body_lf, textvariable = self.body_name_var).grid(row = 0, column = 1, columnspan=3, sticky=tk.W)

        tk.Label(setup_body_lf, text="Position").grid(row = 1, column = 0)
        tk.Entry(setup_body_lf, textvariable = self.body_position_x_var).grid(row = 1, column = 1)
        tk.Entry(setup_body_lf, textvariable = self.body_position_y_var).grid(row = 1, column = 2)
        tk.Entry(setup_body_lf, textvariable = self.body_position_z_var).grid(row = 1, column = 3)

        tk.Label(setup_body_lf, text="Velocity").grid(row = 2, column = 0)
        tk.Entry(setup_body_lf, textvariable = self.body_velocity_x_var).grid(row = 2, column = 1)
        tk.Entry(setup_body_lf, textvariable = self.body_velocity_y_var).grid(row = 2, column = 2)
        tk.Entry(setup_body_lf, textvariable = self.body_velocity_z_var).grid(row = 2, column = 3)

        tk.Label(setup_body_lf, text="Mass").grid(row = 3, column = 0)
        tk.Entry(setup_body_lf, textvariable = self.body_mass_var).grid(row = 3, column = 1, columnspan=3, sticky=tk.W)

        tk.Label(setup_body_lf, text="Radius").grid(row = 4, column = 0)
        tk.Entry(setup_body_lf, textvariable = self.body_radius_var).grid(row = 4, column = 1, columnspan=3, sticky=tk.W)

        tk.Button(setup_body_lf, text="Create or update", command=self.__create_and_send_body).grid(row = 5, column = 0, columnspan=4, pady=5)

        return setup_body_lf

    def __setup_configuration_frame(self):
        configuration_lf = tk.LabelFrame(self.root, text="Configuration")

        tk.Checkbutton(configuration_lf, variable = self.coordinate_axes_enabled_var, onvalue = True, offvalue = False, text = "Show coordinates axes", command = self.send_configuration).grid(row = 0, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.compass_enabled_var, onvalue = True, offvalue = False, text = "Show compass", command = self.send_configuration).grid(row = 1, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.orbits_enabled_var, onvalue = True, offvalue = False, text = "Show orbits", command = self.send_configuration).grid(row = 2, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.barycentrum_enabled_var, onvalue = True, offvalue = False, text = "Calibrate barycentrum to zero", command = self.__calibrate_barycentrum_to_zero).grid(row = 3, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.velocity_enabled_var, onvalue = True, offvalue = False, text = "Show velocities", command = self.send_configuration).grid(row = 4, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.movement_var, onvalue = True, offvalue = False, text = "Movement", command = self.send_configuration).grid(row = 5, column = 0, sticky="W", padx = 10)
        return configuration_lf

    def __setup_camera_frame(self):
        camera_lf = tk.LabelFrame(self.root, text="Camera")

        tk.Button(camera_lf, text="Set HOME camera", width = 15, command=lambda: self.send_command(Command.SET_HOME_CAMERA)).grid(row = 0, column = 0, padx = 10, pady=5)
        tk.Button(camera_lf, text="Set OX camera", width = 15, command=lambda: self.send_command(Command.SET_POSITION_OX_CAMERA)).grid(row = 1, column = 0, padx = 10, pady=5)
        tk.Button(camera_lf, text="Set OY camera", width = 15, command=lambda: self.send_command(Command.SET_POSITION_OY_CAMERA)).grid(row = 2, column = 0, padx = 10, pady=5)
        tk.Button(camera_lf, text="Set OZ camera", width = 15, command=lambda: self.send_command(Command.SET_POSITION_OZ_CAMERA)).grid(row = 3, column = 0, padx = 10, pady=5)
        
        return camera_lf
    
    def __create_and_send_body(self):
        data = {
            "body_name": self.body_name_var.get(),
            "body_position": (self.body_position_x_var.get(), self.body_position_y_var.get(), self.body_position_z_var.get()),
            "body_velocity": (self.body_velocity_x_var.get(), self.body_velocity_y_var.get(), self.body_velocity_z_var.get()),
            "body_mass": self.body_mass_var.get(),
            "body_radius": self.body_radius_var.get()
        }

        self.send_command_with_data(Command.CREATE_OR_UPDATE_BODY, data)

    def __setup_body_info(self):
        body_info_lf = tk.LabelFrame(self.root, text="Body / Orbit info")
        body_frame = tk.Frame(body_info_lf)
        body_frame.id="welcome"
        tk.Label(body_frame, text="Here will appear of your body info").grid(row = 0, column = 0, padx = 10, pady=5)
        body_frame.grid(row = 0, column = 0)
        return body_info_lf

    def send_configuration(self):
        data = {
            "show_coordinate_axes": self.coordinate_axes_enabled_var.get(),
            "show_compass": self.compass_enabled_var.get(),
            "show_orbits": self.orbits_enabled_var.get(),
            "show_velocities": self.velocity_enabled_var.get(),
            "movement": self.movement_var.get()
        }
        self.send_command_with_data(Command.SET_CONFIGURATION, data)

    def synchronize_bodies(self, bodies):
        # TODO: this should be refactored
        if len(bodies) > 0:
            for body_frame in self.body_info.winfo_children():
                if body_frame.id=="welcome":
                    body_frame.destroy()
                    break

        for body_frame in self.body_info.winfo_children():
            found = False
            for body in bodies:
                if body_frame.id == body.name:
                    found = True
                    break
            if not found:
                body_frame.destroy()

        for body in bodies:
            found = False
            for body_frame in self.body_info.winfo_children():
                if body_frame.id!=body.name:
                    continue
                found = True
                for w in body_frame.winfo_children():
                    try:
                        id = w.id
                    except:
                        continue
                    if w.id =="position":
                        w["text"] = f"Position: <{round(body.position.x)}, {round(body.position.y)}, {round(body.position.z)}>"
                        continue
                    if w.id =="velocity":
                        w["text"] = f"Velocity: <{round(body.velocity.x)}, {round(body.velocity.y)}, {round(body.velocity.z)}>"
                        continue
                    if w.id =="mass":
                        w["text"] = f"Mass: {round(body.mass)}"
                        continue
                    if w.id =="revolving":
                        w["text"] = f"Revolving: {body.center_body_name}"
                        continue
                    if w.id =="shape":
                        w["text"] = f"Shape: {body.orbit.shape}"
                        continue
                    if w.id =="a":
                        w["text"] = f"Semi major axis: {round(body.orbit.semi_major_axis)}"
                        continue
                    if w.id =="b":
                        w["text"] = f"Semi minor axis: {round(body.orbit.semi_minor_axis)}"
                        continue
                    if w.id =="e":
                        w["text"] = f"Eccentricity: {round(body.orbit.eccentricity, 4)}"
                        continue
                    if w.id =="phi":
                        w["text"] = f"True anomaly: {round(math.degrees(body.orbit.true_anomaly))}"
                        continue
                
            if not found:
                body_frame = tk.Frame(self.body_info)
                body_frame.id = body.name
                tk.Label(body_frame, text=f"Name: {body.name}").grid(row = 0, column = 0, sticky=tk.W)
                l_position = tk.Label(body_frame, text=f"Position: <{round(body.position.x)}, {round(body.position.y)}, {round(body.position.z)}>")
                l_position.id = "position"
                l_position.grid(row = 1, column = 0, sticky=tk.W)
                l_velocity = tk.Label(body_frame, text=f"Velocity: <{round(body.velocity.x)}, {round(body.velocity.y)}, {round(body.velocity.z)}>")
                l_velocity.id = "velocity"
                l_velocity.grid(row = 2, column = 0, sticky=tk.W)
                l_mass = tk.Label(body_frame, text=f"Mass: {round(body.mass)}")
                l_mass.id = "mass"
                l_mass.grid(row = 3, column = 0, sticky=tk.W)
                if body.type == BodyType.SPHERE:
                    l_radius = tk.Label(body_frame, text=f"Radius: {round(body.radius)}")
                    l_radius.id = "radius"
                    l_radius.grid(row = 4, column = 0, sticky=tk.W)
                l_revolving = tk.Label(body_frame, text=f"Revolving: {body.center_body_name}")
                l_revolving.id = "revolving"
                l_revolving.grid(row = 5, column = 0, sticky=tk.W)
                if body.has_orbit:
                    l_shape = tk.Label(body_frame, text=f"Shape: {body.orbit.shape}")
                    l_shape.id = "shape"
                    l_shape.grid(row = 1, column = 1, sticky=tk.W)
                    l_a = tk.Label(body_frame, text=f"Semi major axis: {round(body.orbit.semi_major_axis)}")
                    l_a.id = "a"
                    l_a.grid(row = 2, column = 1, sticky=tk.W)
                    l_b = tk.Label(body_frame, text=f"Semi minor axis: {round(body.orbit.semi_minor_axis)}")
                    l_b.id = "b"
                    l_b.grid(row = 3, column = 1, sticky=tk.W)
                    l_e = tk.Label(body_frame, text=f"Eccentricity: {round(body.orbit.eccentricity, 4)}")
                    l_e.id = "e"
                    l_e.grid(row = 4, column = 1, sticky=tk.W)
                    l_phi = tk.Label(body_frame, text=f"True anomaly: {round(math.degrees(body.orbit.true_anomaly))}")
                    l_phi.id = "phi"
                    l_phi.grid(row = 5, column = 1, sticky=tk.W)
                tk.Button(body_frame, text=f"Remove {body.name}", command=lambda id=body.name: self.remove_body(id)).grid(row = 6, column = 0)
                tk.Button(body_frame, text=f"Focus on {body.name}", command=lambda id=body.name: self.focus_on_body(id)).grid(row = 6, column = 1)
                body_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky=tk.W)

        row = 0
        for body_frame in self.body_info.winfo_children():
            body_frame.grid(row = row, column = 0, padx = 10, pady = 10, sticky=tk.W)
            row += 1
    
    def remove_body(self, name):
        self.send_command_with_data(Command.REMOVE_BODY, data = name)

    def focus_on_body(self, name):
        self.send_command_with_data(Command.FOCUS_ON_BODY, data = name)

    def __calibrate_barycentrum_to_zero(self):
        self.send_command_with_data(Command.CALIBRATE_BARYCENTRUM_TO_ZERO, self.barycentrum_enabled_var.get())