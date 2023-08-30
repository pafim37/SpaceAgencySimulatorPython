from models.orbit import Orbit
import numpy as np
import math
from ursina import *
from models.body_system import BodySystem
from models.body import Body
from models.reference_system import ReferenceSystem
from models.compass import Compass
from models.config import Config
import time
import quaternion
from tk_form import TkForm
from mediator import Mediator
import logging
from urs_form import UrsForm
from commands import *

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