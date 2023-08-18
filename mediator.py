from commands import *
from models.body import Body
import logging
import numpy as np
from ursina import *

class Mediator:
    def __init__(self):
        self.camera = None
        self.log = logging.getLogger(__name__)

    def register_tk_form(self, tk_form):
        self.tk_form = tk_form

    def register_urs_form(self, urs_form):
        self.urs_form = urs_form

    def register_body_system(self, body_system):
        self.body_system = body_system

    def register_config(self, config):
        self.config = config

    def send(self, command, data = None):
        match command:
            case Command.CREATE_OR_UPDATE_BODY:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_body_from_dict(data)
                self.log.info(f"End handle {command}")
                return
            case Command.HANDLE_SUN:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_or_remove_sun()
                self.__synchronize_bodies_and_orbits()
                self.log.info(f"End handle {command}")
                return
            case Command.HANDLE_EARTH:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_or_remove_earth()
                self.__synchronize_bodies_and_orbits()
                self.log.info(f"End handle {command}")
                return
            case Command.HANDLE_MARS:
                self.log.info(f"Starting handle {command}")
                self.body_system.add_or_remove_mars()
                self.__synchronize_bodies_and_orbits()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_HOME_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.urs_form.go_home_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OX_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.urs_form.set_position_ox_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OY_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.urs_form.set_position_oy_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_POSITION_OZ_CAMERA:
                self.log.info(f"Starting handle {command}")
                self.urs_form.set_position_oz_camera()
                self.log.info(f"End handle {command}")
                return
            case Command.SET_CONFIGURATION:
                self.log.info(f"Starting handle {command}")
                self.config.set_configuration(data)
                self.urs_form.set_configuration(self.config)
                self.log.info(f"End handle {command}")
                return
            case _:
                self.log.info(f"Did not found {command}")
        return
        
    def __synchronize_bodies_and_orbits(self):
        self.urs_form.synchronize_bodies(self.body_system.get_bodies())
        self.urs_form.synchronize_orbits(self.body_system.get_orbits())