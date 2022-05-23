import unittest

from main import World


class TestWorld(unittest.TestCase):
    def test_foo(self):
        world = World()
        self.assertIsNotNone(world)
