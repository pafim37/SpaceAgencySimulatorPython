import tkinter as tk
from commands import *

class TkForm:
    def __init__(self):
        self.root = tk.Tk()
        self.__setup_root()
        self.__create_variables()
        self.__setup_frames()

    def register_mediator(self, mediator):
        self.mediator = mediator

    def send_command(self, command):
        self.mediator.send(command)
    
    def send_command_with_data(self, command, data):
        self.mediator.send(command, data)

    def update_root(self):
        self.root.update()

    def __setup_root(self):
        self.root.title("Setup panel")

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

        self.coordinate_axes_enabled_var  = tk.BooleanVar(self.root, True)
        self.compass_enabled_var = tk.BooleanVar(self.root, True)

    def __setup_frames(self):
        body_frame = self.__setup_body_frame()
        default_body_frame = self.__setup_default_body_frame()
        configuration_frame = self.__setup_configuration_frame()
        camera_frame = self._setup_camera_frame()
        
        body_frame.grid(row = 0, column = 0, padx = 10, pady=10)
        default_body_frame.grid(row = 1, column = 0, padx = 10, pady=10)
        configuration_frame.grid(row = 2, column = 0, padx = 10, pady=10)
        camera_frame.grid(row = 3, column = 0, padx = 10, pady=10)


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

    def __setup_default_body_frame(self):
        body_default_lf = tk.LabelFrame(self.root, text="Add body")

        btn_ids = []

        add_sun_btn = tk.Button(body_default_lf, text="Add Sun", width = 15, command=lambda: self.__handle_create_command(Command.CREATE_SUN, 0, btn_ids))
        add_sun_btn.grid(row = 0, column = 0, padx = 10, pady=5)
        add_earth_btn = tk.Button(body_default_lf, text="Add Earth", width = 15, command=lambda: self.__handle_create_command(Command.CREATE_EARTH, 1, btn_ids))
        add_earth_btn.grid(row = 1, column = 0, padx = 10, pady=5)
        add_mars_btn = tk.Button(body_default_lf, text="Add Mars", width = 15, command=lambda: self.__handle_create_command(Command.CREATE_MARS, 2, btn_ids))
        add_mars_btn.grid(row = 2, column = 0, padx = 10, pady=5)

        btn_ids.append(add_sun_btn)
        btn_ids.append(add_earth_btn)
        btn_ids.append(add_mars_btn)

        return body_default_lf

    def __setup_configuration_frame(self):
        configuration_lf = tk.LabelFrame(self.root, text="Configuration")

        tk.Checkbutton(configuration_lf, variable = self.coordinate_axes_enabled_var, onvalue = True, offvalue = False, text = "Show coordinates axes", command = self.send_configuration).grid(row = 0, column = 0, sticky="W", padx = 10)
        tk.Checkbutton(configuration_lf, variable = self.compass_enabled_var, onvalue = True, offvalue = False, text = "Show compass", command = self.send_configuration).grid(row = 1, column = 0, sticky="W", padx = 10)
        
        return configuration_lf

    def _setup_camera_frame(self):
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

    def send_configuration(self):
        data = {
            "show_coordinate_axes": self.coordinate_axes_enabled_var.get(),
            "show_compass": self.compass_enabled_var.get(),
        }
        self.send_command_with_data(Command.SET_CONFIGURATION, data)

    def __handle_create_command(self, command, btn_id, btn_ids):
        self.send_command(command)
        actual_text = btn_ids[btn_id]["text"]
        actual_text_array = actual_text.split(" ")
        body_name = actual_text_array[1]
        verb = actual_text_array[0]
        if verb == "Add":
            btn_ids[btn_id]["text"] = "Remove " + body_name
        elif verb == "Remove":
            btn_ids[btn_id]["text"] = "Add " + body_name



