from models.orbits.orbit import Orbit
import numpy as np
import math
from ursina import *
from models.bodies.body_system import BodySystem
from models.reference_system import ReferenceSystem
from models.compass import Compass
from models.config import Config
import time
import quaternion
from forms.tk_form import TkForm
from mediator.mediator import Mediator
import logging
from forms.urs_form import UrsForm
from mediator.commands import *
from models.bodies.add_body_handler import AddBodyHandler

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  
    ]
)

class App:
    def __init__(self):
        self.urs_form = UrsForm()
        self.tk_form = TkForm()
        self.config = Config()
        self.body_system = BodySystem(1) # TODO: configure G
        AddBodyHandler.add_planets(self.body_system)
        AddBodyHandler.add_shuttle(self.body_system)

        self.mediator = Mediator()
        self.tk_form.register_mediator(self.mediator)
        self.urs_form.register_mediator(self.mediator)
        self.body_system.register_mediator(self.mediator) 
        self.config.register_mediator(self.mediator) 

        self.urs_form.assign_player()

        self.tk_form.send_configuration()
        self.mediator.send(Command.UPDATE)
        self.mediator.send(Command.SET_POSITION_OZ_CAMERA)

    def run(self):
        running = True
        while running:
            self.tk_form.update()
            self.urs_form.update()
            if self.config.movement:
                self.mediator.send(Command.UPDATE, False)
            

if __name__ == '__main__':
    app = App()
    app.run()