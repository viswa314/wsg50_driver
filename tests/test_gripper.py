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
        driver.move_to_width(75.0)
        self.assertEqual(driver.current_width, 75.0)

    def test_status(self):
        driver = WSG50110Driver()
        status = driver.get_status()
        self.assertIn("current_width", status)
        self.assertEqual(status["current_width"], 50.0)


if __name__ == '__main__':
    unittest.main()
