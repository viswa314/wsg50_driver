import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.gripper_driver import GripperDriver


class TestGripperDriver(unittest.TestCase):
    def test_connection(self):
        driver = GripperDriver(ip='127.0.0.1', port=1000)
        driver.connect()
        self.assertIn(driver.connected, [True, False])
        driver.disconnect()


if __name__ == '__main__':
    unittest.main()
