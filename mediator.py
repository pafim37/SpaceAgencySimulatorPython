from commands import *
from models.body import Body
import logging
import numpy as np
from ursina import *

class Mediator:
    def __init__(self):
        self.camera = None
        self.body_system = None
        self.log = logging.getLogger(__name__)
        self.is_body_system_synchronize_with_entities = False

    def send(self, command, data = None):
        match command:
            case Command.CREATE_OR_UPDATE_BODY:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_body_from_dict(data)
                self.is_body_system_synchronize_with_entities = False
                self.log.info(f"End handle {command}")
                return
            case Command.CREATE_SUN:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_sun()
                self.is_body_system_synchronize_with_entities = False
                self.log.info(f"End handle {command}")
                return
            case Command.CREATE_EARTH:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_earth()
                self.is_body_system_synchronize_with_entities = False
                self.log.info(f"End handle {command}")
                return
            case Command.CREATE_MARS:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_mars()
                self.is_body_system_synchronize_with_entities = False
                self.log.info(f"End handle {command}")
                return
            case Command.SET_HOME_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.__go_home_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OX_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.__set_position_ox_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OY_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.__set_position_oy_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OZ_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.__set_position_oz_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_CONFIGURATION:
                self.log.info(f"Starting handle {command}")
                self.__set_configuration(data)
                self.log.info(f"End handle {command}")
                return
        return
        
    def __set_configuration(self, data):
        self.show_coordinate_axes = data["show_coordinate_axes"]
        self.show_compass = data["show_compass"]

    def __go_home_camera(self):
        self.camera.position = (5, 5, -5)
        self.camera.rotation = (35, -45, 0)

    def __set_position_ox_camera(self):
        self.camera.position = (-10, 0, 0)
        self.camera.rotation = (0, 90, -90)    

    def __set_position_oy_camera(self):
        self.camera.position = (0, 10, 0)
        self.camera.rotation = (90, 0, 0)

    def __set_position_oz_camera(self):
        self.camera.position = (0, 0, -10)
        self.camera.rotation = (0, 0, 0)