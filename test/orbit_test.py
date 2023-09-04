import unittest
from models.orbit import Orbit
from models.body import Body
from models.bodies.body_system import BodySystem
import numpy as np
import math

class TestClass(unittest.TestCase):
    def test_orbit_zero(self):
        body_system = BodySystem(1)
        sun = Body(name = "Sun", position = np.zeros(3), velocity = np.zeros(3), mass = 10000, radius = 1)
        body = Body(name = "Planet", position = np.array([50, 0, 0]), velocity = np.array([0, 17, 0]), mass = 1, radius = 1)
        body_system.add_body(sun)
        body_system.add_body(body)
        orbit = body_system.get_orbits()[0]
        
        self.assertEqual(0.0, orbit.phi)
        self.assertEqual(0.0, orbit.i)
        self.assertEqual(0.0, orbit.true_longitude)

if __name__=='__main__':
	unittest.main()