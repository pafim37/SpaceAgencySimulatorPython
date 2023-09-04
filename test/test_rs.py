import unittest
from models.reference_system import ReferenceSystem
import numpy as np
import math

class TestClass(unittest.TestCase):
    def test_get_angles_100(self):
        x, y, z = ReferenceSystem.get_angles(np.array([1, 0, 0]))
        
        self.assertEqual(0.0, x)
        self.assertEqual(0.0, y)
        self.assertEqual(0.0, z)

    def test_get_angles_010(self):
        x, y, z = ReferenceSystem.get_angles(np.array([0, 1, 0]))
        
        self.assertEqual(0.0, x)
        self.assertEqual(0.0, y)
        self.assertEqual(90.0, z)

    def test_get_angles_001(self):
        x, y, z = ReferenceSystem.get_angles(np.array([0, 0, 1]))
        
        self.assertEqual(0.0, x)
        self.assertEqual(90.0, y)
        self.assertEqual(0.0, z)

    def test_get_angles_001(self):
        x, y, z = ReferenceSystem.get_angles(np.array([1, 1, 1]))
        
        self.assertEqual(-9.5908, x)
        self.assertEqual(30.0, y)
        self.assertEqual(35.0, z)

if __name__=='__main__':
	unittest.main()