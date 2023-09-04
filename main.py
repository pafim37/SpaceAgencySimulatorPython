from models.orbits.orbit import Orbit
import numpy as np
import math
from ursina import *
from models.bodies.body_system import BodySystem
from models.bodies.body import Body
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

        mediator = Mediator()
        self.tk_form.register_mediator(mediator)
        self.urs_form.register_mediator(mediator)
        self.body_system.register_mediator(mediator) 
        self.config.register_mediator(mediator) 

        self.tk_form.send_configuration()
        mediator.send(Command.UPDATE)

    def run(self):
        running = True
        while running:
            self.tk_form.update()
            self.urs_form.update()

if __name__ == '__main__':
    app = App()
    app.run()