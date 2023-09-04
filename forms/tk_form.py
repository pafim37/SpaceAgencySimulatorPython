import tkinter as tk
from mediator.commands import *
import math

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

    def __setup_root(self):
        self.root.title("Setup panel")
        self.root.geometry("720x700")

    def __create_variables(self):
        self.body_name_var = tk.StringVar(self.root, "Earth")
        self.body_position_x_var = tk.DoubleVar(self.root, 50)
        self.body_position_y_var = tk.DoubleVar(self.root, 50)
        self.body_position_z_var = tk.DoubleVar(self.root, 0)
        self.body_velocity_x_var = tk.DoubleVar(self.root, 5)
        self.body_velocity_y_var = tk.DoubleVar(self.root, 0)
        self.body_velocity_z_var = tk.DoubleVar(self.root, 0)
        self.body_mass_var = tk.DoubleVar(self.root, 1)
        self.body_radius_var = tk.DoubleVar(self.root, 1)

        self.coordinate_axes_enabled_var  = tk.BooleanVar(self.root, False)
        self.compass_enabled_var = tk.BooleanVar(self.root, False)
        self.orbits_enabled_var = tk.BooleanVar(self.root, False)
        self.velocity_enabled_var = tk.BooleanVar(self.root, False)
        self.barycentrum_enabled_var = tk.BooleanVar(self.root, False)

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
        tk.Label(body_frame, text="Here will appear of your body info").grid(row = 0, column = 0, padx = 10, pady=5)
        body_frame.grid(row = 0, column = 0)
        return body_info_lf

    def send_configuration(self):
        data = {
            "show_coordinate_axes": self.coordinate_axes_enabled_var.get(),
            "show_compass": self.compass_enabled_var.get(),
            "show_orbits": self.orbits_enabled_var.get(),
            "show_velocities": self.velocity_enabled_var.get()
        }
        self.send_command_with_data(Command.SET_CONFIGURATION, data)

    def synchronize_bodies_and_orbits(self, bodies, orbits):
        for widget in self.body_info.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        row = 0
        for body in bodies:
            body_frame = tk.Frame(self.body_info)

            tk.Label(body_frame, text=f"Name: {body.name}").grid(row = 0, column = 0, sticky=tk.W)
            tk.Label(body_frame, text=f"Position: <{round(body.position[0])}, {round(body.position[1])}, {round(body.position[2])}>").grid(row = 1, column = 0, sticky=tk.W)
            tk.Label(body_frame, text=f"Velocity: <{round(body.velocity[0])}, {round(body.velocity[1])}, {round(body.velocity[2])}>").grid(row = 2, column = 0, sticky=tk.W)
            tk.Label(body_frame, text=f"Mass: {round(body.mass)}").grid(row = 3, column = 0, sticky=tk.W)
            tk.Label(body_frame, text=f"Radius: {round(body.radius)}").grid(row = 4, column = 0, sticky=tk.W)
            tk.Label(body_frame, text=f"Revolving: {body.center_body_name}").grid(row = 5, column = 0, sticky=tk.W)
            orbit = [orbit for orbit in orbits if body.name == orbit.name]
            if len(orbit) > 0:
                orbit = orbit[0]
                tk.Label(body_frame, text=f"Shape: {orbit.shape}").grid(row = 1, column = 1, sticky=tk.W)
                tk.Label(body_frame, text=f"Semi major axis: {round(orbit.semi_major_axis)}").grid(row = 2, column = 1, sticky=tk.W)
                tk.Label(body_frame, text=f"Semi minor axis: {round(orbit.semi_minor_axis)}").grid(row = 3, column = 1, sticky=tk.W)
                tk.Label(body_frame, text=f"Eccentricity: {round(orbit.eccentricity, 4)}").grid(row = 4, column = 1, sticky=tk.W)
                tk.Label(body_frame, text=f"True anomaly: {round(math.degrees(orbit.true_anomaly))}").grid(row = 5, column = 1, sticky=tk.W)
            
            tk.Button(body_frame, text=f"Remove {body.name}", command=lambda id=body.name: self.remove_body(id)).grid(row = 6, column = 0)
            tk.Button(body_frame, text=f"Focus on {body.name}", command=lambda id=body.name: self.focus_on_body(id)).grid(row = 6, column = 1)
            body_frame.grid(row = row, column = 0, padx = 10, pady = 10, sticky=tk.W)
            row += 1
    
    def remove_body(self, name):
        self.send_command_with_data(Command.REMOVE_BODY, data = name)

    def focus_on_body(self, name):
        self.send_command_with_data(Command.FOCUS_ON_BODY, data = name)

    def __calibrate_barycentrum_to_zero(self):
        self.send_command_with_data(Command.CALIBRATE_BARYCENTRUM_TO_ZERO, self.barycentrum_enabled_var.get())