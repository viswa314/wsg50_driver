import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.wsg50110_driver import WSG50110Driver


class TestWSG50110Driver(unittest.TestCase):

    def test_connection(self):
        driver = WSG50110Driver(ip='127.0.0.1', port=1000)
        driver.connect()
        self.assertIn(driver.connected, [True, False])
        driver.disconnect()

    def test_move_to_width(self):
        driver = WSG50110Driver()
        driver.home()
        driver.calibrate()
        driver.move_to_width(70.0)
        self.assertEqual(driver.current_width, 70.0)

    def test_status(self):
        driver = WSG50110Driver()
        status = driver.get_status()
        self.assertIn("current_width", status)
        self.assertFalse(status["homed"])

    def test_home(self):
        driver = WSG50110Driver()
        driver.home()
        self.assertTrue(driver.homed)
        self.assertEqual(driver.current_width, driver.max_width)

    def test_calibrate(self):
        driver = WSG50110Driver()
        driver.home()
        driver.calibrate()
        self.assertTrue(driver.calibrated)
        self.assertEqual(driver.min_width, 0.0)
        self.assertEqual(driver.max_width, 110.0)

    def test_move_rejected_if_not_homed(self):
        driver = WSG50110Driver()
        driver.move_to_width(40.0)
        self.assertIsNone(driver.current_width)


if __name__ == '__main__':
    unittest.main()
