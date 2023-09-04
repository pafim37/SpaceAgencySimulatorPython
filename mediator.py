from commands import *
from models.bodies.body import Body
import logging
import numpy as np
from ursina import *
from converters.body_converter import BodyConverter

class Mediator:
    def __init__(self):
        self.camera = None
        self.log = logging.getLogger(__name__)

    # TODO: create interface for those components
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
                # TODO: add logs here Debug
                body = BodyConverter.from_dictionary(data)
                self.body_system.add_or_update_body(body)
                self.__update_body_system_on_backend_and_frontend()
                self.log.info(f"End handle {command}")
                return
            case Command.REMOVE_BODY:
                self.log.info(f"Starting handle {command}")
                self.body_system.remove_body_by_name(data)
                self.__update_body_system_on_backend_and_frontend()
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
            case Command.CALIBRATE_BARYCENTRUM_TO_ZERO:
                self.log.info(f"Starting handle {command}")
                self.body_system.calibrate_barycentrum = data
                self.__update_body_system_on_backend_and_frontend()
                self.log.info(f"End handle {command}")
                return
            case Command.UPDATE:
                self.__update_body_system_on_backend_and_frontend()
                return
            case Command.FOCUS_ON_BODY:
                self.__update_body_system_on_backend_and_frontend()
                self.urs_form.set_position_camera(data)
                return
            case _:
                self.log.info(f"Did not found {command}")
                return
        return

    def __update_body_system_on_backend_and_frontend(self):
        self.body_system.update()
        bodies = self.body_system.get_bodies()
        orbits = self.body_system.get_orbits()
        self.tk_form.synchronize_bodies_and_orbits(bodies, orbits)
        self.urs_form.synchronize_bodies_and_orbits(bodies, orbits)