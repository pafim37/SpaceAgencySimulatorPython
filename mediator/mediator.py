from mediator.commands import *
import logging
import numpy as np
from ursina import *
from converters.body_converter import BodyConverter

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
            case Command.THRUST_PLAYER:
                self.body_system.thrust_shuttle(data)
                return
            case Command.GET_PLAYER:
                return self.body_system.get_player()
            case Command.CREATE_OR_UPDATE_BODY:
                self.log.info(f"Starting handle {command}")
                # TODO: add logs here Debug
                body = BodyConverter.from_dictionary(data)
                self.body_system.add_or_update_body(body)
                self.body_system.update_orbit()
                self.log.info(f"End handle {command}")
                return
            case Command.REMOVE_BODY:
                self.log.info(f"Starting handle {command}")
                self.body_system.remove_body_by_name(data)
                self.body_system.update_orbit()
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
                self.body_system.movement = self.config.movement
                self.log.info(f"End handle {command}")
                return
            case Command.CALIBRATE_BARYCENTRUM_TO_ZERO:
                self.log.info(f"Starting handle {command}")
                self.body_system.calibrate_barycentrum = data
                self.body_system.update_orbit()
                self.log.info(f"End handle {command}")
                return
            case Command.FOCUS_ON_BODY:
                self.urs_form.set_position_camera(data)
                return
            case _:
                self.log.info(f"Did not found {command}")
                return
        return

    def __update_body_system_on_backend_and_frontend(self):
        bodies = self.body_system.get_bodies()
        self.tk_form.synchronize_bodies(bodies)
        self.urs_form.synchronize_bodies(bodies)